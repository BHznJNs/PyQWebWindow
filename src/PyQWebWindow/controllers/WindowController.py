import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

from PyQWebWindow.utils import get_caller_file_abs_path

class WindowController:
    def __init__(self,
        title    : str  | None,
        icon     : str  | None,
        resizable: bool | None,
    ):
        self._window = QMainWindow(None)
        self._resizable = True
        self._on_top = False
        if title     is not None: self.title     = title
        if icon      is not None: self.icon      = icon
        if resizable is not None: self.resizable = resizable

    def _window_fill_with_browser_widget(self, browser_widget: QWebEngineView):
        self._window.setCentralWidget(browser_widget)

    @property
    def window(self) -> QMainWindow:
        return self._window

    @property
    def title(self) -> str:
        return self._window.windowTitle()
    @title.setter
    def title(self, title: str):
        self._window.setWindowTitle(title)

    @property
    def icon(self): raise AttributeError("Cannot access 'icon' directly.")
    @icon.setter
    def icon(self, path: str):
        if os.path.isabs(path):
            target_path = path
        else:
            caller_path = get_caller_file_abs_path()
            caller_dir_path = os.path.dirname(caller_path)
            target_path = os.path.join(caller_dir_path, os.path.normpath(path))
        icon = QIcon(target_path)
        self._window.setWindowIcon(icon)

    """ window size getter & setter begin """
    @property
    def width(self) -> int:
        return self._window.width()
    @width.setter
    def width(self, new_val: int):
        self._window.resize(new_val, self.height)
    @property
    def height(self) -> int:
        return self._window.height()
    @height.setter
    def height(self, new_val: int):
        self._window.resize(self.width, new_val)

    @property
    def minimum_size(self) -> tuple[int, int]:
        size = self._window.minimumSize()
        return (size.width(), size.height())
    @minimum_size.setter
    def minimum_size(self, width: int, height: int):
        self._window.setMinimumSize(QSize(width, height))
    @property
    def maximum_size(self) -> tuple[int, int]:
        size = self._window.maximumSize()
        return (size.width(), size.height())
    @maximum_size.setter
    def maximum_size(self, width: int, height: int):
        self._window.setMaximumSize(QSize(width, height))

    @property
    def resizable(self) -> bool:
        return self._resizable
    @resizable.setter
    def resizable(self, new_val: bool):
        MAX_SIZE = 16777215
        self._resizable = new_val
        window = self._window
        if new_val:
            window.setMinimumSize(QSize(0, 0))
            window.setMaximumSize(QSize(MAX_SIZE, MAX_SIZE))
        else: window.setFixedSize(window.size())
    """ window size getter & setter end """
    
    """ window position getter & setter begin """
    @property
    def x(self) -> int:
        """Relative from the left side of screen"""
        return self._window.pos().x()
    @property
    def y(self) -> int:
        """Relative from the top side of screen"""
        return self._window.pos().y()
    
    def move(self, x: int, y: int):
        self._window.move(x, y)
    """ window position getter & setter end """


    """ window operations begin """
    def show (self): self._window.show()
    def hide (self): self._window.hide()
    def close(self): self._window.close()
    def focus(self):
        self._window.raise_()
        self._window.activateWindow()

    @property
    def on_top(self) -> bool:
        return self._on_top
    @on_top.setter
    def on_top(self, new_val: bool):
        self._on_top = new_val
        self._window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, new_val)
        self._window.show()

    @property
    def hidden(self) -> bool:
        return self._window.isHidden()
    @property
    def minimized(self) -> bool:
        return self._window.isMinimized()
    @property
    def maximized(self) -> bool:
        return self._window.isMaximized()
    @property
    def fullscreened(self) -> bool:
        return self._window.isFullScreen()

    def minimize(self):
        self._window.showMinimized()
    def restore(self):
        self._window.showNormal()
    def maximize(self):
        self._window.showMaximized()
    def fullscreen(self):
        self._window.showFullScreen()
    """ window operations end """
