import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.PyQWebWindow import QWebWindow

def launch_test():
    """
    There should be a blank window appear after invocate this function.
    """
    window = QWebWindow()
    window.launch()

def launch_with_debug_test():
    """
    There should be a blank window appear after invocate this function while logs in console:

    > DevTools listening on ws://127.0.0.1:9222/devtools/browser/e10719bb-3fb5-4f7e-a0b4-8bf5eafbd6fb  
    > Remote debugging server started successfully. Try pointing a Chromium-based browser to http://127.0.0.1:9222

    """
    window = QWebWindow(debugging=True)
    window.launch()

def set_html_test():
    """
    There should be a window appear with a headline: `Hello World!`
    """
    window = QWebWindow()
    window.set_html("<h1>Hello World!</h1>")
    window.launch()
