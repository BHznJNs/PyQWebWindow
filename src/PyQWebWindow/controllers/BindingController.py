from typing import Callable, Union, TypeAlias
from PySide6.QtCore import QObject
from PySide6.QtWebChannel import QWebChannel

Serializable: TypeAlias = Union[
    int, float, bool, str, None,
    list["Serializable"], tuple["Serializable", ...], dict["Serializable", "Serializable"], QObject]
SerializableCallable: TypeAlias = Callable[..., Serializable]

class BindingController:
    from ..QWorker import QWorker

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

    def register_worker(self, worker: QWorker):
        self._backend.add_worker(worker)
    def register_workers(self, workers: list[QWorker]):
        for worker in workers: self._backend.add_worker(worker)
