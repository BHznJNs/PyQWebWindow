import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QWebWindow, QAppManager, Slot

def launch_test():
    """
    There should be a blank window appear after invocate this function.
    """
    window = QWebWindow()
    window.show()
    return window

def set_html_test():
    """
    There should be a window appear with a headline: `Hello World!`
    """
    window = QWebWindow()
    window.set_html("<h1>Hello World!</h1>")
    window.show()
    return window

def load_page_test():
    window = QWebWindow()
    window.load_file("pages/helloworld.html")
    window.show()
    return window

def load_page_with_assets_test():
    window = QWebWindow()
    window.load_file("pages/load_assets.html")
    window.show()
    return window

def load_url_test():
    window = QWebWindow()
    window.load_url("https://github.com")
    window.show()
    return window

def python_binding_test():
    def helloworld(): return "Hello World!"
    def hello_user(user_name: str): return f"Hello {user_name}!"

    window = QWebWindow()
    window.load_file("pages/python_binding.html")
    window.register_bindings([helloworld, hello_user])
    window.show()
    return window

def eval_js_test():
    window = QWebWindow()
    window.show()
    window.eval_js("document.write('<h1>Inserted text by eval</h1>')")
    return window

app = QAppManager(debugging=True)
window = python_binding_test()
app.exec()
