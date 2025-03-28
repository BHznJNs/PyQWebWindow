from .controllers import BrowserController, BindingController, WindowController
from .EventListener import EventListener
from .utils import INITIAL_SCRIPT

class QWebWindow(BrowserController, BindingController, WindowController):
    def __init__(self):
        super().__init__()
        self._window_fill_with_browser_widget(self._browser)
        self._init_handler()

    def _init_handler(self):
        event_listener = self.event_listener = EventListener()
        event_listener.add_event_listener("load_finished",
                                          lambda _: self.eval_js(INITIAL_SCRIPT))
        self._browser_load_finished.connect(event_listener.on_load_finished)
        self._browser_visible_changed.connect(event_listener.on_visible_changed)
        self._browser_window_close_requested.connect(event_listener.on_window_close_request)

    def show(self):
        if not self._browser_has_bound_channel:
            self._binding_register_backend()
            self._browser_bind_channel(self._channel)
        super().show()

    def focus(self):
        super().focus()
        self._browser.setFocus()
