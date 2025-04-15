from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from threading import Lock
from ..utils.Serializable import Serializable, SerializableCallable

@dataclass
class IpcEvent:
    callback: SerializableCallable
    is_once: bool = False

class IpcEventEmitter(ABC):
    def __init__(self):
        super().__init__()
        self._event_dict: dict[str, list[IpcEvent]] = defaultdict(list)

    def _call_event(self, event_name: str, args: list[Serializable]):
        events = self._event_dict[event_name]
        for event in events: event.callback(*args)
        self._remove_once(event_name)

    def _remove_once(self, event_name: str):
        events = self._event_dict.setdefault(event_name, [])
        if len(events) == 0: return
        self._event_dict[event_name] = list(filter(lambda e: not e.is_once, events))

    def on(self, event_name: str, callback: SerializableCallable):
        self._event_dict.setdefault(event_name, [])
        self._event_dict[event_name].append(IpcEvent(callback))

    def once(self, event_name: str, callback: SerializableCallable):
        self._event_dict.setdefault(event_name, [])
        self._event_dict[event_name].append(IpcEvent(callback, is_once=True))

    def off(self, event_name: str, callback: SerializableCallable):
        events = self._event_dict.setdefault(event_name, [])
        if len(events) == 0: return
        for i in range(0, len(events)):
            if events[i].callback is not callback: continue
            events.pop(i); break

    @abstractmethod
    def emit(self, event_name: str, *args: Serializable): pass

class IpcAEventEmitter(IpcEventEmitter):
    """
    Atomic Event Emitter
    """
    def __init__(self):
        super().__init__()
        self._lock = Lock()

    def _remove_once(self, event_name: str):
        with self._lock:
            return super()._remove_once(event_name)

    def on(self, event_name: str, callback: SerializableCallable):
        with self._lock: super().on(event_name, callback)

    def once(self, event_name: str, callback: SerializableCallable):
        with self._lock: super().once(event_name, callback)

    def off(self, event_name: str, callback: SerializableCallable):
        with self._lock: super().off(event_name, callback)
