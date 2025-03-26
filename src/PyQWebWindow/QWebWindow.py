import os

from typing import Callable
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl
from .Backend import Backend
from .Handler import Handler
from .utils import INITIAL_SCRIPT, get_caller_file_abs_path

class QWebWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self._backend = Backend()
        self._channel = QWebChannel()
        self._browser = QWebEngineView()
        self.setCentralWidget(self._browser)
        self._init_handler()

    def _init_handler(self):
        handler = self.handler = Handler()
        handler.add_event_listener("load_finished",
                                   lambda _: self.eval_js(INITIAL_SCRIPT))
        self._browser.page().loadFinished.connect(handler.on_load_finished)

    def set_html(self, html: str):
        self._browser.setHtml(html)

    def load_file(self, path: str):
        """load file
        Args:
            path (str): the relative path to the caller file
        """
        caller_path = get_caller_file_abs_path()
        caller_dir_path = os.path.dirname(caller_path)
        target_path = os.path.join(caller_dir_path, os.path.normpath(path))
        qurl = QUrl.fromLocalFile(target_path)
        self._browser.load(qurl)

    def load_url(self, url: str):
        self._browser.load(QUrl(url))

    def register_binding(self, method: Callable):
        self._backend.add_method(method)
    
    def register_bindings(self, methods: list[Callable]):
        for method in methods: self.register_binding(method)

    def eval_js(self, script: str):
        self._browser.page().runJavaScript(script)

    def show(self):
        has_bound_channel = self._browser.page().webChannel() is not None
        if not has_bound_channel:
            self._channel.registerObject("backend", self._backend)
            self._browser.page().setWebChannel(self._channel)
        super().show()
