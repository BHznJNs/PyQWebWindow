import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow.all import QWebWindow, QAppManager

def load_html_test():
    window = QWebWindow()
    window.load_html("<h1>Hello World!</h1>")
    window.start()
    return window

def load_page_test():
    window = QWebWindow()
    window.load_file("pages/helloworld.html")
    window.start()
    return window

def load_page_with_assets_test():
    window = QWebWindow()
    window.load_file("pages/load_assets.html")
    window.start()
    return window

def load_url_test():
    window = QWebWindow()
    window.load_url("https://github.com")
    window.start()
    return window

def open_link_test():
    window = QWebWindow()
    window.load_file("pages/open_link.html")
    window.start()
    return window

def browser_events_test():
    def load_finished_handler(ok: bool): print("load finished:", ok)
    def visible_changed_handler(visible: bool): print("visible changed:", visible)
    def window_close_requested_handler(): print("window close requested")
    window = QWebWindow()
    window.event_listener.add_event_listener("load_finished", load_finished_handler)
    window.event_listener.add_event_listener("visible_changed", visible_changed_handler)
    window.event_listener.add_event_listener("window_close_requested", window_close_requested_handler)
    window.start()
    return window

def eval_js_test():
    window = QWebWindow()
    window.start()
    window.eval_js("document.write('<h1>Inserted text by eval</h1>')")
    return window

def python_binding_test():
    def helloworld(): return "Hello World!"
    def hello_user(user_name: str): return f"Hello {user_name}!"

    window = QWebWindow()
    window.load_file("pages/python_binding.html")
    window.register_bindings([helloworld, hello_user])
    window.start()
    return window

def python_worker_test():
    """
    After the window appear 3 seconds, there should appear three alert, shows:
    "Hello user1!"
    "Hello user2!"
    "Hello user3!"
    The order is not fixed.
    """
    def task(user_name: str) -> str:
        from time import sleep
        sleep(3)
        return f"Hello {user_name}!"

    window = QWebWindow()
    window.load_file("pages/python_worker.html")
    window.register_task(task)
    window.start()
    return window

app = QAppManager(debugging=True)
window = python_worker_test()
app.exec()
