import sys
import os
from multiprocessing import freeze_support

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QAppManager, QIpcServer, QIpcClient, IpcServer

def qipc_event_emit():
    def event(bar: str):
        print("server received: ", bar)
        assert bar == "bar"
        app.quit()

    server = QIpcServer()
    server.on("foo", event)
    client = QIpcClient(server.server_name)
    client.emit("foo", "bar")
    app = QAppManager()
    app.exec()

def qipc_event_emit_on():
    """
    Expected output:
    bar1
    foo2
    """
    def server_event(bar: str):
        assert bar == "bar1"
        print(bar)
        server.emit("bar1", "foo2")

    def client_event(foo: str):
        assert foo == "foo2"
        print(foo)
        app.quit()

    server = QIpcServer()
    server.on("foo1", server_event)
    client = QIpcClient(server.server_name)
    client.on("bar1", client_event)
    client.emit("foo1", "bar1")

    app = QAppManager()
    app.exec()

qipc_event_emit_on()
