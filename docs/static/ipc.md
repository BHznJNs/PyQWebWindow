# IPC (Inter-Process Communication)

PyQWebWindow supports IPC using two methods: ZeroMQ (`MqIpc`) and Qt's `QLocalSocket` (`QIpc`). This is useful for communication between the main GUI process and other Python processes.

## ZeroMQ IPC (`IpcServer`, `IpcClient`)

```python
# Example using MqIpc (ZeroMQ)
# See examples/ipc.py for a complete working example with multiprocessing.

from PyQWebWindow.all import IpcServer, IpcClient

# Server side
server = IpcServer(daemon=False)
server.on("message_from_client", lambda data: print("Server received:", data))
server.start()
# server.emit("message_to_client", {"status": "ready"})
# server.stop()

# Client side (used within a QWebWindow process)
# from PyQWebWindow.all import QWebWindow, QAppManager, IpcClient
# app = QAppManager()
# window = QWebWindow()
# client = IpcClient() # Connects to the default port
# client.on("message_from_server", lambda data: print("Client received:", data))
# client.connected.connect(lambda: client.emit("message_to_client", "Hello from client"))
# window.use_ipc_client(client)
# window.start()
# app.exec()
# client.stop()
```

## Qt Local Socket IPC (`QIpcServer`, `QIpcClient`)

```python
# Example using QIpc (Qt Local Socket)
# See examples/qipc.py for a complete working example.

from PyQWebWindow.all import QIpcServer, QIpcClient

# Server side
server = QIpcServer(server_name="my_unique_server_name")
server.on("message_from_client", lambda data: print("Server received:", data))
# server.start() # QIpcServer starts automatically on creation
# server.emit("message_to_client", "Hello from server")
# server.stop()

# Client side
# from PyQWebWindow.all import QAppManager, QIpcClient
# app = QAppManager()
# client = QIpcClient(server_name="my_unique_server_name")
# client.on("message_from_server", lambda data: print("Client received:", data))
# client.emit("message_to_server", "Hello from client")
# app.exec()
```

You can use `window.use_ipc_server(server)` or `window.use_ipc_client(client)` to integrate IPC with a `QWebWindow`.
