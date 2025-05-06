# Window Management

You can control the `QWebWindow`'s appearance and behavior using its properties and methods:

```python
from PyQWebWindow.all import QWebWindow, QAppManager

app = QAppManager()
window = QWebWindow()
window.start()

# Set/Get window title
window.title = "New Title"
print(window.title)

# Set window icon (path relative to caller file or absolute)
window.icon = "path/to/icon.png"

# Set/Get window size
window.size = (1024, 768)
print(window.width, window.height)

# Set/Get minimum/maximum size
window.minimum_size = (300, 200)
window.maximum_size = (1600, 1200)

# Set/Get window position
window.pos = (200, 200)
print(window.x, window.y)
window.move(250, 250) # Move to specific coordinates

# Control resizability
window.resizable = False # Make window fixed size

# Control "always on top"
window.on_top = True

# Show/Hide/Close the window
window.show()
window.hide()
window.close()

# Minimize/Maximize/Fullscreen/Restore
window.minimize()
window.maximize()
window.fullscreen()
window.restore()

# Check window state
print(window.hidden, window.minimized, window.maximized, window.fullscreened)

# Focus the window
window.focus()

app.exec()
