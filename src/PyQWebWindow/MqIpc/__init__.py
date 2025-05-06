"""MqIpc
The `MqIpc` module uses pyzmq for the IPC server, instead of `QLocalServer`.
So that this module should be used when not wanting to start QApplication in the main process.
"""

DEFAULT_IPC_PORT = 5556
