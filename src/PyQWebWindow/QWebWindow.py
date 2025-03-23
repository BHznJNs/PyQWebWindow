from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class QWebWindow(QMainWindow):
    _app: QApplication
    _browser: QWebEngineView

    _args = ["--webEngineArgs"]

    def __init__(self,
        debugging: bool = False,
        debugging_port: int = 9222,
    ):
        if debugging:
            self._args.append(f"--remote-debugging-port={debugging_port}")
            self._args.append("--remote-allow-origins=*")
        self._app = QApplication(self._args)

        super().__init__()
        self._browser = QWebEngineView()
        self.setCentralWidget(self._browser)

    def set_html(self, html: str):
        self._browser.setHtml(html)

    def load_page(self, url: str):
        self._browser.load(url)

    def launch(self):
        self.show()
        self._app.exec()
