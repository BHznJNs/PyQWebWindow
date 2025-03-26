from typing import Callable
from PySide6.QtCore import QObject, Slot, Property

class Backend(QObject):
    def __init__(self):
        super().__init__(None)
        self._method_dict: dict[str, Callable] = {}

    def add_method(self, method: Callable):
        method_name = method.__name__
        self._method_dict[method_name] = method

    @Property(list)
    def _methods(self):
        return list(self._method_dict.keys())

    @Slot(str, 'QVariant', result='QVariant')
    def _dispatch(self, method_name, args):
        if method_name in self._method_dict:
            return self._method_dict[method_name](*args)
