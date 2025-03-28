from typing import Callable
from PySide6.QtWebChannel import QWebChannel
from PyQWebWindow.Backend import Backend

class BindingController:
    def __init__(self):
        self._backend = Backend()
        self._channel = QWebChannel()

    def _binding_register_backend(self):
        self._channel.registerObject("backend", self._backend)

    def register_binding(self, method: Callable):
        self._backend.add_method(method)

    def register_bindings(self, methods: list[Callable]):
        for method in methods: self.register_binding(method)
