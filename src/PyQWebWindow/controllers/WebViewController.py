import os

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from ..utils import get_caller_file_abs_path

class CustomWebEnginePage(QWebEnginePage):
    class BrowserBridgePage(QWebEnginePage):
        """
        This class is used to open links from the WebEngine in user default browser.
        Especially for `<a href="http://example.com" target="_blank"></a>`
        """
        def __init__(self, parent=None):
            super().__init__(parent)
            self.urlChanged.connect(self._on_url_changed)

        def _on_url_changed(self, url: QUrl):
            # open url with user default browser
            QDesktopServices.openUrl(url)
            self.deleteLater()

    def createWindow(self, type_: QWebEnginePage.WebWindowType): # type: ignore
        match type_:
            case QWebEnginePage.WebWindowType.WebBrowserWindow |\
                 QWebEnginePage.WebWindowType.WebBrowserTab    |\
                 QWebEnginePage.WebWindowType.WebBrowserBackgroundTab:
                return CustomWebEnginePage.BrowserBridgePage(self)
            case QWebEnginePage.WebWindowType.WebDialog:
                return super().createWindow(type_)
            case _: raise ValueError("Unexpected WebWindowType: ", type_)

class WebViewController:
    def __init__(self,
        enable_clipboard    : bool,
        enable_javascript   : bool,
        enable_localstorage : bool,
        enable_webgl        : bool,
        force_darkmode      : bool,
        show_scrollbars     : bool,
        parent              : QWidget,
    ):
        self._webview = QWebEngineView(parent)
        self._webpage = CustomWebEnginePage(self._webview)
        self._webview.setPage(self._webpage)

        settings = self._webpage.settings()
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
        return self._webpage.webChannel() is not None

    def _webview_bind_channel(self, channel: QWebChannel):
        self._webpage.setWebChannel(channel)

    @property
    def webview(self) -> QWebEngineView:
        return self._webview

    @property
    def webpage(self) -> QWebEnginePage:
        return self._webpage

    def load_html(self, html: str):
        self._webpage.setHtml(html)

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
        self._webpage.load(qurl)

    def load_url(self, url: str):
        self._webpage.load(QUrl(url))

    def eval_js(self, *scripts: str):
        for script in scripts:
            self._webpage.runJavaScript(script)
