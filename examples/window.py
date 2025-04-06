import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QWebWindow, QAppManager

def launch_test():
    """
    There should be a blank window appear after invocate this function.
    """
    window = QWebWindow()
    window.start()
    return window

def set_title_test():
    window = QWebWindow()
    window.title = "test title"
    window.start()
    return window

def hide_when_close_test():
    window = QWebWindow(hide_when_close=True)
    window.start()
    return window

app = QAppManager(debugging=True)
window = launch_test()
app.exec()
