# PyQWebWindow

Another way to build Python Webview GUI applications.

## Getting started

### Install

```bash
pip install PyQWebWindow
```

### Hello world

```python
from PyQWebWindow import QWebWindow, QAppManager

app = QAppManager(debugging=True)
window = QWebWindow()
window.set_html("<h1>Hello World!</h1>")
window.start()
app.exec()
```

## Development

### Run Tests

```shell
pytest tests
```
