import uuid
import threading
import zmq

from . import DEFAULT_IPC_PORT
from ..EventEmitter import IpcAEventEmitter
from ..Serializer import IpcSerializer
from ...utils import Serializable

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

        def _process_message(self, client_id: bytes, message: bytes):
            self._clients.add(client_id)
            if message == b"reg": return # process registration message

            message_parsed: list[Serializable] = IpcSerializer.loads(message)
            event_name = str(message_parsed[0])
            args = message_parsed[1:]
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

                if client_received:
                    try: client_id, message = self._server_socket.recv_multipart(zmq.NOBLOCK)
                    except zmq.error.ContextTerminated: break
                    except (zmq.error.Again, zmq.error.ZMQError): continue
                    self._process_message(client_id, message)

                if inproc_received:
                    try: bytes_message = self._inproc_socket.recv(zmq.NOBLOCK)
                    except zmq.error.ContextTerminated: break
                    except (zmq.error.Again, zmq.error.ZMQError): continue

                    assert type(bytes_message) is bytes
                    # send to all clients
                    for client_id in self._clients:
                        self._send_message(client_id, bytes_message)

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
