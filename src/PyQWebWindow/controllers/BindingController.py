from typing import Callable, Union
from PySide6.QtCore import QObject
from PySide6.QtWebChannel import QWebChannel

class BindingController:
    Serializable = Union[
        int, float, bool, str, None,
        list["Serializable"], tuple["Serializable", ...], dict["Serializable", "Serializable"], QObject]
    SerializableCallable = Callable[..., Serializable]

    def __init__(self):
        from .Backend import Backend
        self._backend = Backend()
        self._channel = QWebChannel()

    def _binding_register_backend(self):
        self._channel.registerObject("backend", self._backend)

    def register_binding(self, method: SerializableCallable):
        self._backend.add_method(method)

    def register_bindings(self, methods: list[SerializableCallable]):
        for method in methods: self.register_binding(method)
