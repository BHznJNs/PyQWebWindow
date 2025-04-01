from typing import Callable
from PySide6.QtCore import QObject, Signal, Slot, Property

from PyQWebWindow import QWorker, Serializable, SerializableCallable

class Backend(QObject):
    _worker_finished = Signal("QVariant") # type: ignore

    def __init__(self):
        super().__init__(None)
        self._worker_dict: dict[str, QWorker] = {}
        self._method_dict: dict[str, SerializableCallable] = {}

    def add_worker(self, worker: QWorker):
        self._worker_dict[worker.name] = worker

    def add_method(self, method: Callable):
        method_name = method.__name__
        self._method_dict[method_name] = method

    @Property(list)
    def _workers(self):
        return list(self._worker_dict.keys())

    @Slot(str, list)
    def _start_worker(self,
        worker_name: str,
        args: list[Serializable],
    ):
        worker = self._worker_dict[worker_name]
        worker.set_args(args)
        worker.finished.connect(lambda result:
            self._worker_finished.emit(result))
        worker.start()

    @Property(list)
    def _methods(self):
        return list(self._method_dict.keys())

    @Slot(str, list, result="QVariant") # type: ignore
    def _dispatch(self, method_name: str, args: list[Serializable]):
        if method_name in self._method_dict:
            return self._method_dict[method_name](*args)
