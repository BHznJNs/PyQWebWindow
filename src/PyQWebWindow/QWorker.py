from PySide6.QtCore import QThread, Signal

class QWorker(QThread):
    from PyQWebWindow.controllers.BindingController import Serializable, SerializableCallable

    finished = Signal(type(Serializable))

    def __init__(self, task: SerializableCallable):
        super().__init__(None)
        self._task = task

    @property
    def name(self):
        return self._task.__name__
    
    def set_args(self, args: list[Serializable]):
        self._args = args

    def run(self):
        result = self._task(*self._args)
        self.finished.emit(result)
