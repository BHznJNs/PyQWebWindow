import uuid
from PySide6.QtCore import QObject
from PySide6.QtNetwork import QLocalServer, QLocalSocket

from ..Serializer import IpcSerializer
from ..EventEmitter import IpcEventEmitter
from ...utils.Serializable import Serializable

class QIpcServer(IpcEventEmitter):
    def __init__(self, server_name: str = str(uuid.uuid4())):
        super().__init__()
        self._clients: set[QLocalSocket] = set()
        self.server_name = server_name
        QIpcServer.ensure_server_name(server_name)

        server = self._server = QLocalServer()
        if not server.listen(server_name):
            err = server.errorString()
            raise RuntimeError(f"Cannot listen {server_name}: {err}")
        server.newConnection.connect(self._handle_connection)

    def _use_parent(self, parent: QObject):
        self._server.setParent(parent)

    @staticmethod
    def ensure_server_name(server_name: str):
        """
        Ensure the passed in `server_name` is not taken
        """
        try: QLocalServer.removeServer(server_name)
        except Exception: pass

    def _handle_connection(self):
        client = self._server.nextPendingConnection()
        self._clients.add(client)
        client.readyRead.connect(lambda: self._handle_event(client))
        client.disconnected.connect(lambda s=client: self._handle_disconnected(s))

    def _handle_disconnected(self, client: QLocalSocket):
        self._clients.remove(client)
        client.deleteLater()

    def _handle_event(self, client: QLocalSocket):
        while client.bytesAvailable():
            data = client.readAll().data()
            decoded: list[Serializable] = IpcSerializer.loads(data)
            event_name = str(decoded[0])
            args = decoded[1:]
            self._call_event(event_name, args)

    def emit(self, event_name: str, *args: Serializable):
        encoded = IpcSerializer.dumps([event_name, *args])
        for client in self._clients:
            client.write(encoded)

    def close(self):
        self._server.close()
        QLocalServer.removeServer(self.server_name)
