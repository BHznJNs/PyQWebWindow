from PySide6.QtCore import QObject
from PySide6.QtNetwork import QLocalSocket

from ..utils import Serializable
from ..utils.Serializer import IpcSerializer
from ..utils.EventEmitter import IpcEventEmitter

class QIpcClient(IpcEventEmitter):
    connect_timeout_ms = 300

    def __init__(self, server_name: str):
        super().__init__()
        socket = self._socket = QLocalSocket()
        socket.connectToServer(server_name)
        if not socket.waitForConnected(QIpcClient.connect_timeout_ms):
            raise RuntimeError(f"Cannot connect to server {server_name}, is server on?")
        socket.readyRead.connect(self._handle_event)

    def _use_parent(self, parent: QObject):
        self._socket.setParent(parent)

    def _handle_event(self):
        while self._socket.bytesAvailable():
            data = self._socket.readAll().data()
            decoded: list[Serializable] = IpcSerializer.loads(data)
            event_name = str(decoded[0])
            args = decoded[1:]
            self._call_event(event_name, args)

    def emit(self, event_name: str, *args: Serializable):
        encoded = IpcSerializer.dumps([event_name, *args])
        self._socket.write(encoded)

    def close(self):
        self._socket.disconnectFromServer()
