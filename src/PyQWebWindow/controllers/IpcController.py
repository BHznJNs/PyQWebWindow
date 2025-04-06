import pickle
import uuid
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from ..utils.Serializable import Serializable, SerializableCallable

class IpcPayload:
    @staticmethod
    def dumps(obj: Serializable):
        return pickle.dumps(obj)
    @staticmethod
    def loads(data: bytes):
        return pickle.loads(data)

class IpcServer:
    def __init__(self, server_name: str = str(uuid.uuid4())):
        self._event_dict: dict[str, list[SerializableCallable]] = {}
        self._clients: set[QLocalSocket] = set()
        self.server_name = server_name
        IpcServer.ensure_server_name(server_name)

        server = self._server = QLocalServer()
        if not server.listen(server_name):
            err = server.errorString()
            raise RuntimeError(f"Cannot listen {server_name}: {err}")
        server.newConnection.connect(self._handle_connection)

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
            decoded: list[Serializable] = IpcPayload.loads(data)
            event_name = str(decoded[0])
            args = decoded[1:]
            events = self._event_dict[event_name]
            for event in events: event(*args)

    def on(self, event_name: str, callback: SerializableCallable):
        self._event_dict.setdefault(event_name, [])
        self._event_dict[event_name].append(callback)

    def emit(self, event_name: str, *args: Serializable):
        encoded = IpcPayload.dumps([event_name, *args])
        for client in self._clients:
            client.write(encoded)

    def close(self):
        self._server.close()
        QLocalServer.removeServer(self.server_name)

class IpcClient:
    connect_timeout_ms = 300

    def __init__(self, server_name: str):
        self._event_dict: dict[str, list[SerializableCallable]] = {}
        socket = self._socket = QLocalSocket()
        socket.connectToServer(server_name)
        if not socket.waitForConnected(IpcClient.connect_timeout_ms):
            raise RuntimeError(f"Cannot connect to server {server_name}, is server on?")
        socket.readyRead.connect(self._handle_event)

    def _handle_event(self):
        while self._socket.bytesAvailable():
            data = self._socket.readAll().data()
            decoded: list[Serializable] = IpcPayload.loads(data)
            event_name = str(decoded[0])
            args = decoded[1:]
            events = self._event_dict[event_name]
            for event in events: event(*args)

    def on(self, event_name: str, callback: SerializableCallable):
        self._event_dict.setdefault(event_name, [])
        self._event_dict[event_name].append(callback)

    def emit(self, event_name: str, *args: Serializable):
        encoded = IpcPayload.dumps([event_name, *args])
        self._socket.write(encoded)

    def close(self):
        self._socket.disconnectFromServer()
