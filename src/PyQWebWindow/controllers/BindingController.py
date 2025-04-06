from PySide6.QtWebChannel import QWebChannel

class BindingController:
    from ..QWorker import QWorker
    from ..utils.Serializable import SerializableCallable

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

    def register_task(self, task: SerializableCallable):
        self._backend.add_task(task)
    def register_tasks(self, tasks: list[SerializableCallable]):
        for task in tasks: self._backend.add_task(task)
