from .controllers import WebViewController, BindingController, WindowController
from .EventListener import EventListener
from .QContextMenu import QContextMenu
from .ipc.QIpc.server import QIpcServer
from .ipc.QIpc.client import QIpcClient
from .ipc.MqIpc.client import IpcClient
from .utils import INITIAL_SCRIPT, LOADED_SCRIPT

class QWebWindow(WebViewController, BindingController, WindowController):
    def __init__(self,
        # params below are window options
        title: str  | None = None,
        icon : str  | None = None,
        pos  : tuple[int, int] | None = None,
        size : tuple[int, int] | None = None,
        minimum_size: tuple[int, int] | None = None,
        maximum_size: tuple[int, int] | None = None,
        resizable: bool = True,
        on_top   : bool = False,
        hide_when_close: bool = False,
        # params below are webview options
        background_color: str | None = None,
        enable_clipboard    : bool = True,
        enable_javascript   : bool = True,
        enable_localstorage : bool = True,
        enable_webgl        : bool = True,
        force_darkmode      : bool = False,
        show_scrollbars     : bool = True,
    ):
        WindowController.__init__(self,
            title, icon, pos, size,
            minimum_size, maximum_size,
            resizable, on_top, hide_when_close)
        WebViewController.__init__(self,
            background_color,
            enable_clipboard, enable_javascript, enable_localstorage,
            enable_webgl, force_darkmode, show_scrollbars, self._window)
        BindingController.__init__(self, self._window)
        self._window_fill_with_browser_widget(self._webview)
        self._init_event_listener()
        self._ipc_client = None

    def _init_event_listener(self):
        event_listener = self.event_listener = EventListener()
        event_listener.add_event_listener("load_started",
            lambda: self.eval_js(INITIAL_SCRIPT))
        event_listener.add_event_listener("load_finished",
            lambda _: self.eval_js(LOADED_SCRIPT))
        webpage = self.webpage
        window  = self.window
        webpage.loadStarted.connect(event_listener.on_load_started)
        webpage.loadFinished.connect(event_listener.on_load_finished)
        webpage.visibleChanged.connect(event_listener.on_visible_changed)
        webpage.windowCloseRequested.connect(event_listener.on_window_close_requested)
        window.resized.connect(event_listener.on_window_resized)
        window.shown.connect(event_listener.on_window_shown)
        window.hidden.connect(event_listener.on_window_hidden)
        window.closed.connect(event_listener.on_window_closed)

    def use_context_menu(self, menu: QContextMenu):
        from PySide6.QtCore import Qt, QPoint
        def show_contextmenu(pos: QPoint):
            nonlocal menu, webview
            global_pos = webview.mapToGlobal(pos)
            menu._show(webview, global_pos)

        webview = self._webview
        webview.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        webview.customContextMenuRequested.connect(show_contextmenu)

    def use_ipc_server(self, server: QIpcServer):
        server._use_parent(self._window)

    def use_ipc_client(self, client: IpcClient | QIpcClient):
        if type(client) is QIpcClient:
            client._use_parent(self._window)
            return
        assert type(client) is IpcClient
        client._setup_worker(self._window)
        self.event_listener\
            .add_event_listener("window_closed", lambda: client.stop())

    def start(self, show_when_ready: bool = True):
        self._binding_register_backend()
        self._webview_bind_channel(self._channel)
        if show_when_ready: super().show()

    def focus(self):
        super().focus()
        self.webview.setFocus()
