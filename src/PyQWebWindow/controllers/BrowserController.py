import os

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from PyQWebWindow.utils import get_caller_file_abs_path

class BrowserController:
    def __init__(self):
        self._browser = QWebEngineView()

    @property
    def _browser_has_bound_channel(self):
        return self._browser.page().webChannel() is not None

    def _browser_bind_channel(self, channel: QWebChannel):
        self._browser.page().setWebChannel(channel)

    """ browser event signals begin """
    @property
    def _browser_load_finished(self):
        return self._browser.page().loadFinished
    @property
    def _browser_visible_changed(self):
        return self._browser.page().visibleChanged
    @property
    def _browser_window_close_requested(self):
        return self._browser.page().windowCloseRequested
    """ browser event signals end """

    def load_html(self, html: str):
        self._browser.setHtml(html)

    def load_file(self, path: str):
        """load file
        Args:
            path (str): The path to HTML file, it can be:
                - The absolute path
                - The relative path to the caller file
        """
        if os.path.isabs(path):
            target_path = path
        else:
            caller_path = get_caller_file_abs_path()
            caller_dir_path = os.path.dirname(caller_path)
            target_path = os.path.join(caller_dir_path, os.path.normpath(path))
        qurl = QUrl.fromLocalFile(target_path)
        self._browser.load(qurl)

    def load_url(self, url: str):
        self._browser.load(QUrl(url))

    def eval_js(self, script: str):
        self._browser.page().runJavaScript(script)
