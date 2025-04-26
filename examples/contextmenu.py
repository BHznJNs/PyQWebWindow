import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow.all import QWebWindow, QAppManager, QContextMenu

def use_custom_context_menu() -> QWebWindow:
    window = QWebWindow()
    contextmenu = QContextMenu()
    contextmenu.add_actions([
        ("Cut"  , lambda: print("Cutted!")),
        ("Copy" , lambda: print("Copied!")),
        ("Paste", lambda: print("Pasted!")),
    ])
    window.use_context_menu(contextmenu)
    window.start()
    return window

app = QAppManager(debugging=True)
window = use_custom_context_menu()
app.exec()
