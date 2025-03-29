from typing import Callable, Literal
from PySide6.QtCore import QObject, Slot

class EventListener(QObject):
    EventName = Literal[
        "load_finished",
        "visible_changed",
        "window_close_requested",
        "window_resized",
        "window_shown",
        "window_hidden",
        "window_closed",
    ]

    def __init__(self):
        super().__init__(None)
        self._event_dict: dict[EventListener.EventName, list[Callable]] = {
            "load_finished": [],
            "visible_changed": [],
            "window_close_requested": [],
            "window_resized": [],
            "window_shown": [],
            "window_hidden": [],
            "window_closed": [],
        }

    def add_event_listener(self, event_name: EventName, callback: Callable):
        self._event_dict[event_name].append(callback)

    """ browser event listeners begin """
    @Slot(bool)
    def on_load_finished(self, ok: bool):
        for c in self._event_dict["load_finished"]: c(ok)

    @Slot(bool)
    def on_visible_changed(self, visible: bool):
        for c in self._event_dict["visible_changed"]: c(visible)

    @Slot()
    def on_window_close_requested(self):
        """triggered when `window.close` is called in JavaScript"""
        for c in self._event_dict["window_close_requested"]: c()
    """ browser event listeners end """

    """ window event listeners start """
    @Slot(int, int)
    def on_window_resized(self, width: int, height: int):
        for c in self._event_dict["window_resized"]: c(width, height)
    
    @Slot()
    def on_window_shown(self):
        for c in self._event_dict["window_shown"]: c()

    @Slot()
    def on_window_hidden(self):
        for c in self._event_dict["window_hidden"]: c()

    @Slot()
    def on_window_closed(self):
        for c in self._event_dict["window_closed"]: c()
    """ window event listeners end """
