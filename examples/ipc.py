import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QAppManager, IpcServer, IpcClient

def test_event_emit():
    def event(bar: str):
        print("server received: ", bar)
        assert bar == "bar"
        app.quit()

    server = IpcServer()
    server.on("foo", event)
    client = IpcClient(server.server_name)
    client.emit("foo", "bar")
    app = QAppManager()
    app.exec()

def test_event_emit_on():
    def server_event(bar: str):
        assert bar == "bar1"
        print(bar)
        server.emit("bar1", "foo2")

    def client_event(foo: str):
        assert foo == "foo2"
        print(foo)
        app.quit()

    server = IpcServer()
    server.on("foo1", server_event)
    client = IpcClient(server.server_name)
    client.on("bar1", client_event)
    client.emit("foo1", "bar1")

    app = QAppManager()
    app.exec()

test_event_emit_on()
