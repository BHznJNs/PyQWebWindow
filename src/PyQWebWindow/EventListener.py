from typing import Callable, Literal
from PySide6.QtCore import QObject, Slot

class EventListener(QObject):
    EventName = Literal["load_finished", "visible_changed", "window_close_requested"]

    def __init__(self):
        super().__init__(None)
        self._event_dict: dict[EventListener.EventName, list[Callable]] = {
            "load_finished": [],
            "visible_changed": [],
            "window_close_requested": [],
        }

    def add_event_listener(self, event_name: EventName, callback: Callable):
        self._event_dict[event_name].append(callback)

    """ browser event listeners begin """
    @Slot(bool)
    def on_load_finished(self, ok: bool):
        callbacks = self._event_dict["load_finished"]
        for c in callbacks: c(ok)

    @Slot(bool)
    def on_visible_changed(self, visible: bool):
        callbacks = self._event_dict["visible_changed"]
        for c in callbacks: c(visible)

    @Slot()
    def on_window_close_request(self):
        """triggered when `window.close` is called in JavaScript"""
        callbacks = self._event_dict["window_close_requested"]
        for c in callbacks: c()
    """ browser event listeners end """
