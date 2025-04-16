import uuid
import threading
import zmq
import zmq.asyncio

from PySide6.QtCore import QObject, QThread, Signal, Slot, SignalInstance
from .EventEmitter import IpcAEventEmitter
from .Serializer import IpcSerializer
from ..utils import Serializable

DEFAULT_IPC_PORT = 5556

class IpcServer(IpcAEventEmitter):
    class _Worker(threading.Thread):
        def __init__(self,
            context: zmq.Context,
            inproc_addr: str,
            port: int,
            daemon: bool,
            parent: "IpcServer",
        ) -> None:
            super().__init__(daemon=daemon)
            self._inproc_addr = inproc_addr
            self._server_port = port
            self._inproc_socket: zmq.Socket = context.socket(zmq.PULL)
            self._server_socket: zmq.Socket = context.socket(zmq.ROUTER)
            self._clients: set[bytes] = set()
            self._parent = parent
            self.connect_event = threading.Event()
            self.stop_event = threading.Event()

        def _remove_client(self, client_id: bytes):
            if client_id not in self._clients: return
            self._clients.remove(client_id)

        def _send_message(self, client_id: bytes, message_parts: bytes):
            try:
                self._server_socket.send_multipart([
                    client_id, message_parts])
            except zmq.error.ZMQError as e:
                if e.errno in (zmq.ETERM, zmq.ENOTSOCK, zmq.ECONNREFUSED, zmq.ECONNRESET):
                    self._remove_client(client_id)

        def _process_message(self, id: bytes, msg: bytes):
            self._clients.add(id)
            if msg == b"reg": return # process registration message

            msg_parsed: list[Serializable] = IpcSerializer.loads(msg)
            event_name = str(msg_parsed[0])
            args = msg_parsed[1:]
            self._parent._call_event(event_name, args)

        def run(self):
            self._inproc_socket.bind(self._inproc_addr)
            self._server_socket.bind(f"tcp://127.0.0.1:{self._server_port}")
            self.connect_event.set()

            poller = zmq.Poller()
            poller.register(self._inproc_socket, zmq.POLLIN)
            poller.register(self._server_socket, zmq.POLLIN)
            while not self.stop_event.is_set():
                events = poller.poll(100)
                inproc_received = False
                client_received = False
                for socket, event in events:
                    if socket is self._inproc_socket and event & zmq.POLLIN:
                        inproc_received = True
                    if socket is self._server_socket and event & zmq.POLLIN:
                        client_received = True

                if inproc_received:
                    try: bytes_msg = self._inproc_socket.recv(zmq.NOBLOCK)
                    except zmq.error.ContextTerminated: break
                    except (zmq.error.Again, zmq.error.ZMQError): continue

                    assert type(bytes_msg) is bytes
                    # send to all clients
                    for client_id in self._clients:
                        self._send_message(client_id, bytes_msg)
                if client_received:
                    try: id, msg = self._server_socket.recv_multipart(zmq.NOBLOCK)
                    except zmq.error.ContextTerminated: break
                    except (zmq.error.Again, zmq.error.ZMQError): continue
                    self._process_message(id, msg)

            self._inproc_socket.close()
            self._server_socket.close()

    def __init__(self, port: int = DEFAULT_IPC_PORT, daemon: bool = True):
        super().__init__()
        self._is_running = False

        inproc_addr = "inproc://" + str(uuid.uuid4())
        context = self._context = zmq.Context()
        self._inproc_socket = context.socket(zmq.PUSH)
        self._inproc_socket.connect(inproc_addr)
        self._worker = IpcServer._Worker(context, inproc_addr, port, daemon, self)

    def emit(self, event_name: str, *args: Serializable):
        if not self._is_running: return
        encoded = IpcSerializer.dumps([event_name, *args])
        self._inproc_socket.send(encoded)

    def start(self):
        self._worker.start()
        self._worker.connect_event.wait()
        self._is_running = True

    def stop(self):
        if not self._is_running: return
        self._worker.stop_event.set()
        self._inproc_socket.close()
        self._worker.join()
        self._context.term()
        self._is_running = False

class IpcClient(IpcAEventEmitter):
    class _Worker(QThread):
        emitted = Signal(bytes)
        received = Signal(bytes)
        connected = Signal()
        disconnected = Signal()

        def __init__(self, id: str, port: int, poll_timeout: int):
            super().__init__(None)
            self._is_running = False
            self._server_port = port
            self._poll_timeout = poll_timeout
            context = self._context = zmq.Context()
            socket = self._socket = context.socket(zmq.DEALER)
            socket.setsockopt(zmq.IDENTITY, id.encode())
            socket.setsockopt(zmq.LINGER, 0)
            self.emitted.connect(self._send_message)
            self.connected.connect(lambda: self._send_message(b"reg"))

        @Slot(bytes)
        def _send_message(self, message: bytes):
            try: self._socket.send(message)
            except zmq.error.ZMQError:
                self.disconnected.emit()
                self.stop()

        def _receive_message(self) -> bool:
            while True:
                event = self._socket.getsockopt(zmq.EVENTS)
                assert type(event) is int
                if not (event & zmq.POLLIN): break

                try: msg = self._socket.recv(zmq.NOBLOCK)
                except zmq.error.Again: break
                except zmq.error.ContextTerminated: return False
                self.received.emit(msg)
            return True

        def run(self):
            self._is_running = True
            socket = self._socket
            socket.connect(f"tcp://127.0.0.1:{self._server_port}")
            self.connected.emit()
            while self._is_running:
                events = socket.poll(self._poll_timeout, zmq.POLLIN)
                if not (events & zmq.POLLIN): continue
                ret = self._receive_message()
                if not ret: break

            socket.close()
            self._context.term()
            self.disconnected.emit()

        def stop(self):
            self._is_running = False

    def __init__(self,
        id: str = str(uuid.uuid4()),
        port: int = DEFAULT_IPC_PORT,
        poll_timeout: int = 100,
    ):
        super().__init__()
        self._is_connected = False
        worker = self._worker = IpcClient._Worker(id, port, poll_timeout)
        worker.received.connect(self._received_handler)

        def set_is_connected(connected: bool): self._is_connected = connected
        worker.connected.connect(lambda: set_is_connected(True))
        worker.disconnected.connect(lambda: set_is_connected(False))

    def _setup_worker(self, parent: QObject):
        worker = self._worker
        worker.setParent(parent)
        worker.start()

    def _received_handler(self, msg: bytes):
        msg_parsed: list[Serializable] = IpcSerializer.loads(msg)
        event_name = str(msg_parsed[0])
        args = msg_parsed[1:]
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
