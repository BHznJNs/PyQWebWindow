from PySide6.QtWidgets import QApplication
from .QArgv import QArgv

class QAppManager:
    _app_singleton: QApplication | None

    def __init__(self,
        debugging: bool = False,
        debugging_port: int = 9222,
        remote_allow_origin: str = "*"
    ):
        argv = QArgv()
        if debugging:
            argv.set_key("remote-debugging-port", debugging_port)
            argv.set_key("remote-allow-origins", remote_allow_origin)
        QAppManager._app_singleton = QApplication(argv.to_list())

    def exec(self):
        assert QAppManager._app_singleton is not None
        QAppManager._app_singleton.exec()
