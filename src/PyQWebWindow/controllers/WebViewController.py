import os

from PySide6.QtCore import QUrl, SignalInstance
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from PyQWebWindow.utils import get_caller_file_abs_path

class WebViewController:
    def __init__(self,
        enable_clipboard    : bool,
        enable_javascript   : bool,
        enable_localstorage : bool,
        enable_webgl        : bool,
        force_darkmode      : bool,
        show_scrollbars     : bool,
    ):
        self._webview = QWebEngineView()
        settings = self._webview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent    , True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls  , True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, enable_clipboard   )
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled           , enable_javascript  )
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled         , enable_localstorage)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled                , enable_webgl       )
        settings.setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode               , force_darkmode     )
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars              , show_scrollbars    )

    @property
    def _webview_has_bound_channel(self):
        return self._webview.page().webChannel() is not None

    def _webview_bind_channel(self, channel: QWebChannel):
        self._webview.page().setWebChannel(channel)

    @property
    def webview(self) -> QWebEngineView:
        return self._webview

    @property
    def webpage(self) -> QWebEnginePage:
        return self._webview.page()

    def load_html(self, html: str):
        self._webview.setHtml(html)

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
        self._webview.load(qurl)

    def load_url(self, url: str):
        self._webview.load(QUrl(url))

    def eval_js(self, script: str):
        self._webview.page().runJavaScript(script)
