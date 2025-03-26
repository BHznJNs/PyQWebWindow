from typing import Callable, Literal
from PySide6.QtCore import QObject, Slot

EventName = Literal["load_finished"]

class Handler(QObject):
    def __init__(self):
        super().__init__(None)
        self._event_dict: dict[str, list[Callable]] = {
            "load_finished": []
        }

    @Slot(bool)
    def on_load_finished(self, ok):
        callbacks = self._event_dict["load_finished"]
        for c in callbacks: c(ok)

    def add_event_listener(self, event_name: EventName, callback: Callable):
        self._event_dict[event_name].append(callback)
