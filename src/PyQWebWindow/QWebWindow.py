from .controllers import WebViewController, BindingController, WindowController
from .EventListener import EventListener
from .utils import INITIAL_SCRIPT

class QWebWindow(WebViewController, BindingController, WindowController):
    def __init__(self,
        # params below are window options
        title    : str  | None = None,
        icon     : str  | None = None,
        resizable: bool | None = None,
        minimum_size : tuple[int, int] | None = None,
        maximum_size : tuple[int, int] | None = None,
        # params below are webview options
        enable_clipboard    : bool | None = None,
        enable_javascript   : bool | None = None,
        enable_localstorage : bool | None = None,
        enable_webgl        : bool | None = None,
        force_darkmode      : bool | None = None,
        show_scrollbars     : bool | None = None,
    ):
        BindingController.__init__(self)
        WebViewController.__init__(self,
            enable_clipboard, enable_javascript, enable_localstorage,
            enable_webgl, force_darkmode, show_scrollbars)
        WindowController.__init__(self,
            title, icon, resizable, minimum_size, maximum_size)
        self._window_fill_with_browser_widget(self._webview)
        self._init_event_listener()

    def _init_event_listener(self):
        event_listener = self.event_listener = EventListener()
        event_listener.add_event_listener("load_finished",
                                          lambda _: self.eval_js(INITIAL_SCRIPT))
        webpage = self.webpage
        window  = self.window
        webpage.loadFinished.connect(event_listener.on_load_finished)
        webpage.visibleChanged.connect(event_listener.on_visible_changed)
        webpage.windowCloseRequested.connect(event_listener.on_window_close_requested)
        window.resized.connect(event_listener.on_window_resized)
        window.shown.connect(event_listener.on_window_shown)
        window.hidden.connect(event_listener.on_window_hidden)
        window.closed.connect(event_listener.on_window_closed)

    def start(self):
        self._binding_register_backend()
        self._webview_bind_channel(self._channel)
        super().show()

    def focus(self):
        super().focus()
        self.webview.setFocus()
