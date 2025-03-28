from .controllers import WebViewController, BindingController, WindowController
from .EventListener import EventListener
from .utils import INITIAL_SCRIPT

class QWebWindow(WebViewController, BindingController, WindowController):
    def __init__(self,
        title    : str  | None = None,
        icon     : str  | None = None,
        resizable: bool | None = None,
    ):
        WebViewController.__init__(self)
        BindingController.__init__(self)
        WindowController.__init__(self, title, icon, resizable)
        self._window_fill_with_browser_widget(self._webview)
        self._init_handler()

    def _init_handler(self):
        event_listener = self.event_listener = EventListener()
        event_listener.add_event_listener("load_finished",
                                          lambda _: self.eval_js(INITIAL_SCRIPT))
        self._webview_load_finished.connect(event_listener.on_load_finished)
        self._webview_visible_changed.connect(event_listener.on_visible_changed)
        self._webview_window_close_requested.connect(event_listener.on_window_close_request)

    def start(self):
        self._binding_register_backend()
        self._webview_bind_channel(self._channel)
        super().show()

    def focus(self):
        super().focus()
        self._webview.setFocus()
