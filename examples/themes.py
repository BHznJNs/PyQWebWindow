import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QWebWindow, QAppManager

def system_theme():
    app = QAppManager(theme="system")
    window = QWebWindow()
    window.start()
    app.exec()
    return window

def dark_theme():
    app = QAppManager(theme="dark")
    window = QWebWindow()
    window.start()
    app.exec()
    return window

def light_theme():
    app = QAppManager(theme="light")
    window = QWebWindow()
    window.start()
    app.exec()
    return window

light_theme()
