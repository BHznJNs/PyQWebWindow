from typing import Callable
from PySide6.QtCore import QObject, Slot, Property

from PyQWebWindow.controllers import BindingController

class Backend(QObject):
    def __init__(self):
        super().__init__(None)
        self._method_dict: dict[str, BindingController.SerializableCallable] = {}

    def add_method(self, method: Callable):
        method_name = method.__name__
        self._method_dict[method_name] = method

    @Property(list)
    def _methods(self):
        return list(self._method_dict.keys())

    @Slot(str, list, result="QVariant") # type: ignore
    def _dispatch(self, method_name: str, args: list):
        if method_name in self._method_dict:
            return self._method_dict[method_name](*args)
