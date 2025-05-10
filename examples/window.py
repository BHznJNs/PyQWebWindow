import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow.all import QWebWindow, QAppManager

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

def set_background_color_test():
    window = QWebWindow(background_color="#333333")
    window.start()
    return window

def disable_context_menu() -> QWebWindow:
    window = QWebWindow(disable_contextmenu=True)
    # Set the context menu policy to NoContextMenu
    window.start()
    return window

def show_when_ready_test():
    window = QWebWindow()
    window.start(show_when_ready=False)
    return window

def hide_when_close_test():
    window = QWebWindow(hide_when_close=True)
    window.event_listener.add_event_listener("window_closed", lambda: print("closed"))
    window.start()
    return window

app = QAppManager(debugging=True)
window = set_background_color_test()
app.exec()
