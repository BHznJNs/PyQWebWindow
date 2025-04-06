from PySide6.QtCore import QObject, Signal, Slot, Property
from ..QWorker import QWorker
from ..utils.Serializable import Serializable, SerializableCallable

class Backend(QObject):
    _task_finished = Signal(str, "QVariant") # type: ignore

    def __init__(self):
        super().__init__(None)
        # store workers in set to prevent the workers to be cleared by GC
        self._working_workers: set[QWorker] = set()

        self._task_dict: dict[str, SerializableCallable] = {}
        self._method_dict: dict[str, SerializableCallable] = {}

    def add_task(self, task: SerializableCallable):
        task_name = task.__name__
        self._task_dict[task_name] = task

    def add_method(self, method: SerializableCallable):
        method_name = method.__name__
        self._method_dict[method_name] = method

    @Property(list)
    def _tasks(self):
        return list(self._task_dict.keys())

    @Slot(str, str, list)
    def _start_task(self,
        task_name: str,
        callback_name: str,
        args: list[Serializable],
    ):
        def after_worker_finished(result: Serializable):
            nonlocal worker
            self._task_finished.emit(callback_name, result)
            worker.finished.disconnect(after_worker_finished)
            self._working_workers.remove(worker)

        task = self._task_dict[task_name]
        worker = QWorker(task)
        self._working_workers.add(worker)
        worker.set_args(args)
        worker.finished.connect(after_worker_finished)
        worker.start()

    @Property(list)
    def _methods(self):
        return list(self._method_dict.keys())

    @Slot(str, list, result="QVariant") # type: ignore
    def _dispatch(self, method_name: str, args: list[Serializable]):
        if method_name in self._method_dict:
            return self._method_dict[method_name](*args)
