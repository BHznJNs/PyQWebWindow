import uuid
import zmq

from PySide6.QtCore import QObject, QThread, Signal, Slot, SignalInstance
from . import DEFAULT_IPC_PORT
from ..utils import Serializable
from ..utils.EventEmitter import IpcAEventEmitter
from ..utils.Serializer import IpcSerializer

class IpcClient(IpcAEventEmitter):
    class _Worker(QThread):
        emitted = Signal(bytes)
        received = Signal(bytes)
        connected = Signal()
        disconnected = Signal()

        def __init__(self, client_id: str, port: int, poll_timeout: int):
            super().__init__(None)
            self._is_running = False
            self._server_port = port
            self._poll_timeout = poll_timeout
            context = self._context = zmq.Context()
            socket = self._socket = context.socket(zmq.DEALER)
            socket.setsockopt(zmq.IDENTITY, client_id.encode())
            socket.setsockopt(zmq.LINGER, 0)
            self.emitted.connect(self._send_message)
            self.connected.connect(lambda: self._send_message(b"reg"))

        @Slot(bytes)
        def _send_message(self, message: bytes):
            try: self._socket.send(message)
            except zmq.error.ZMQError:
                self.disconnected.emit()
                self.stop()

        def _receive_message(self):
            while True:
                event = self._socket.getsockopt(zmq.EVENTS)
                assert type(event) is int
                if not (event & zmq.POLLIN): break

                try: message = self._socket.recv(zmq.NOBLOCK)
                except zmq.error.Again: break
                except zmq.error.ContextTerminated:
                    self.stop()
                    break
                self.received.emit(message)

        def run(self):
            self._is_running = True
            socket = self._socket
            socket.connect(f"tcp://127.0.0.1:{self._server_port}")
            self.connected.emit()
            while self._is_running:
                events = socket.poll(self._poll_timeout, zmq.POLLIN)
                if not (events & zmq.POLLIN): continue
                self._receive_message()

            socket.close()
            self._context.term()
            self.disconnected.emit()

        def stop(self):
            self._is_running = False

    def __init__(self,
        client_id: str = str(uuid.uuid4()),
        port: int = DEFAULT_IPC_PORT,
        poll_timeout: int = 100,
    ):
        super().__init__()
        self._is_connected = False
        worker = self._worker = IpcClient._Worker(client_id, port, poll_timeout)
        worker.received.connect(self._received_handler)

        def set_is_connected(connected: bool): self._is_connected = connected
        worker.connected.connect(lambda: set_is_connected(True))
        worker.disconnected.connect(lambda: set_is_connected(False))

    def _setup_worker(self, parent: QObject):
        worker = self._worker
        worker.setParent(parent)
        worker.start()

    def _received_handler(self, message: bytes):
        message_parsed: list[Serializable] = IpcSerializer.loads(message)
        event_name = str(message_parsed[0])
        args = message_parsed[1:]
        self._call_event(event_name, args)

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def connected(self) -> SignalInstance:
        return self._worker.connected

    @property
    def disconnected(self) -> SignalInstance:
        return self._worker.disconnected

    def emit(self, event_name: str, *args: Serializable):
        if not self._is_connected: return
        encoded = IpcSerializer.dumps([event_name, *args])
        self._worker.emitted.emit(encoded)

    def stop(self):
        if not self._is_connected: return
        self._worker.stop()
        self._worker.wait()
        self._is_connected = False
