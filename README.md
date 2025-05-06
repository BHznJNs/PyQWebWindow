# PyQWebWindow

Another way to build Python webview GUI applications.

## Getting started

### Install

```bash
pip install PyQWebWindow
```

### Hello world

```python
from PyQWebWindow.all import QWebWindow, QAppManager

app = QAppManager(debugging=True)
window = QWebWindow()
window.set_html("<h1>Hello World!</h1>")
window.start()
app.exec()
```

## Documentation

See [here](https://bhznjns.github.io/PyQWebWindow/) for full documentation.

## Useful Resources

- System tray icon: [pystray](https://github.com/moses-palmer/pystray)
- System dark mode detection: [darkdetect](https://github.com/albertosottile/darkdetect)
- System notification: [notify-py](https://github.com/ms7m/notify-py)
- Clipboard: [pyperclip](https://github.com/asweigart/pyperclip)

## Development

### Run Tests

```shell
pytest tests
```
