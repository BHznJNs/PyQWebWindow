import os

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QCloseEvent, QShowEvent, QHideEvent, QResizeEvent
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

from ..utils import get_caller_file_abs_path

class _MainWindow(QMainWindow):
    resized = Signal(int, int)
    shown   = Signal()
    hidden  = Signal()
    closed  = Signal()

    def __init__(self, hide_when_close: bool) -> None:
        super().__init__(None)
        self._hide_when_close = hide_when_close

    def resizeEvent(self, event: QResizeEvent):
        resized_size = event.size()
        self.resized.emit(resized_size.width(), resized_size.height())
        event.accept()
    def showEvent(self, event: QShowEvent):
        self.shown.emit()
        event.accept()
    def hideEvent(self, event: QHideEvent):
        self.hidden.emit()
        event.accept()
    def closeEvent(self, event: QCloseEvent):
        if self._hide_when_close:
            self.hide()
            event.ignore()
            return
        self.closed.emit()
        event.accept()

class WindowController:
    def __init__(self,
        title: str  | None,
        icon : str  | None,
        pos  : tuple[int, int] | None,
        size : tuple[int, int] | None,
        minimum_size: tuple[int, int] | None,
        maximum_size: tuple[int, int] | None,
        resizable: bool,
        on_top   : bool,
        hide_when_close: bool,
    ):
        self._window = _MainWindow(hide_when_close)
        self.resizable = resizable
        self.on_top = on_top
        if title        is not None: self.title        = title
        if icon         is not None: self.icon         = icon
        if size         is not None: self.size         = size
        if minimum_size is not None: self.minimum_size = minimum_size
        if maximum_size is not None: self.maximum_size = maximum_size
        if pos          is not None: self.pos = pos

    def _window_fill_with_browser_widget(self, browser_widget: QWebEngineView):
        self._window.setCentralWidget(browser_widget)

    @property
    def window(self) -> _MainWindow:
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
    def width(self, new_width: int):
        self._window.resize(new_width, self.height)
    @property
    def height(self) -> int:
        return self._window.height()
    @height.setter
    def height(self, new_height: int):
        self._window.resize(self.width, new_height)

    @property
    def size(self) -> tuple[int, int]:
        size_ = self._window.size()
        return (size_.width(), size_.height())
    @size.setter
    def size(self, new_size: tuple[int, int]):
        self._window.resize(*new_size)
    @property
    def minimum_size(self) -> tuple[int, int]:
        size = self._window.minimumSize()
        return (size.width(), size.height())
    @minimum_size.setter
    def minimum_size(self, size: tuple[int, int]):
        self._window.setMinimumSize(QSize(*size))
    @property
    def maximum_size(self) -> tuple[int, int]:
        size = self._window.maximumSize()
        return (size.width(), size.height())
    @maximum_size.setter
    def maximum_size(self, size: tuple[int, int]):
        self._window.setMaximumSize(QSize(*size))

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

    @property
    def pos(self) -> tuple[int, int]:
        pos_ = self._window.pos()
        return (pos_.x(), pos_.y())
    @pos.setter
    def pos(self, new_pos: tuple[int, int]):
        self._window.move(*new_pos)

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
