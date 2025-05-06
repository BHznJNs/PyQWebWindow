from PySide6.QtCore import QThread, Signal
from .utils.Serializable import Serializable, SerializableCallable

class QWorker(QThread):
    finished = Signal(type(Serializable))

    def __init__(self, task: SerializableCallable, args: list[Serializable]):
        super().__init__(None)
        self._task = task
        self._args = args

    def run(self):
        result = self._task(*self._args)
        self.finished.emit(result)
