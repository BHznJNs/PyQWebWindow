from typing import Literal
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from .QArgv import QArgv

class QAppManager:
    _app_singleton: QApplication | None

    def __init__(self,
        debugging: bool = False,
        debugging_port: int = 9222,
        remote_allow_origin: str = "*",
        theme: Literal["system", "dark", "light"] = "system"
    ):
        if QAppManager._app_singleton is not None: return

        argv = QArgv()
        if debugging:
            argv.set_key("remote-debugging-port", debugging_port)
            argv.set_key("remote-allow-origins", remote_allow_origin)

        QAppManager._app_singleton = QApplication(argv.to_list())
        self.theme = theme

    @staticmethod
    def _parse_theme(theme: str) -> Qt.ColorScheme:
        match theme:
            case "dark" : return Qt.ColorScheme.Dark
            case "light": return Qt.ColorScheme.Light
            case _: return Qt.ColorScheme.Unknown

    @property
    def theme(self) -> str:
        return self._theme
    @theme.setter
    def theme(self, new_theme: Literal["system", "dark", "light"]):
        self._theme = new_theme
        app = QAppManager._app_singleton
        assert app is not None
        app.styleHints().setColorScheme(QAppManager._parse_theme(new_theme))
        app.setPalette(app.palette())

    def exec(self):
        assert QAppManager._app_singleton is not None
        QAppManager._app_singleton.exec()

    def quit(self):
        assert QAppManager._app_singleton is not None
        QAppManager._app_singleton.quit()
