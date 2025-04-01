import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))

from PyQWebWindow import QWebWindow, QAppManager, QWorker

def launch_test():
    """
    There should be a blank window appear after invocate this function.
    """
    window = QWebWindow()
    window.start()
    return window

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

def set_title_test():
    window = QWebWindow()
    window.title = "test title"
    window.start()
    return window

def set_icon_test():
    window = QWebWindow()
    window.icon = ""

def python_binding_test():
    def helloworld(): return "Hello World!"
    def hello_user(user_name: str): return f"Hello {user_name}!"

    window = QWebWindow()
    window.load_file("pages/python_binding.html")
    window.register_bindings([helloworld, hello_user])
    window.start()
    return window

def python_worker_test():
    def task(user_name: str) -> str:
        from time import sleep
        sleep(3)
        return f"Hello {user_name}!"

    window = QWebWindow()
    window.load_file("pages/python_worker.html")
    window.register_worker(QWorker(task))
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

app = QAppManager(debugging=True)
window = python_worker_test()
app.exec()
