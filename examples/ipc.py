import sys
import os
from multiprocessing import Process, freeze_support
from time import sleep

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QAppManager, QWebWindow, IpcServer, IpcClient

def ipc_event_emit_on_child():
    def bar(bar: str):
        print(f"Received message: {bar}")
        client.emit("foo-server2", "bar-server2")

    def exit():
        print("To be exited")
        client.stop()
        window.close()

    app = QAppManager()
    window = QWebWindow()
    client = IpcClient()
    client.on("foo-client", bar)
    client.on("exit", exit)
    client.connected.connect(lambda: client.emit("foo-server1", "bar-server1"))
    client.disconnected.connect(lambda: print("client disconnected"))
    window.use_ipc_client(client)
    window.start()
    app.exec()

def ipc_event_emit_on():
    """
    The web window should appear for a moment and disappear.
    """

    def server_event1(bar: str):
        print("received:", bar)
        assert bar == "bar-server1"
        server.emit("foo-client", "bar-client")

    def server_event2(bar: str):
        print("received:", bar)
        assert bar == "bar-server2"
        server.emit("exit")

    server = IpcServer(daemon=False)
    server.on("foo-server1", server_event1)
    server.on("foo-server2", server_event2)
    server.start()

    proc = Process(target=ipc_event_emit_on_child)
    proc.start()
    proc.join()
    server.stop()

if __name__ == '__main__':
    freeze_support()
    ipc_event_emit_on()
