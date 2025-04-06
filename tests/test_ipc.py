from PyQWebWindow import QAppManager, IpcServer, IpcClient

def test_event_emit():
    """
    In this test, we created a `IpcServer` and a `IpcClient` instance.

    We registered an event on both server and client, and tried to trigger the event.
    """
    def server_event(bar: str):
        assert bar == "bar1"
        server.emit("bar1", "foo2")

    def client_event(foo: str):
        assert foo == "foo2"
        app.quit()

    server = IpcServer()
    server.on("foo1", server_event)
    client = IpcClient(server.server_name)
    client.on("bar1", client_event)
    client.emit("foo1", "bar1")

    app = QAppManager()
    app.exec()
