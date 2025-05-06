# JavaScript Interaction

You can execute JavaScript code in the webview using the `eval_js` method of the `QWebWindow` instance:

```python
from PyQWebWindow.all import QWebWindow, QAppManager

app = QAppManager()
window = QWebWindow()
window.start() # Window must be started before evaluating JavaScript

window.eval_js("alert('Hello from JavaScript!');", "console.log('Another script');")

app.exec()
