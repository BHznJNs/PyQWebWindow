# Core Components

PyQWebWindow is built around two main components: `QAppManager` and `QWebWindow`.

## `QAppManager`

The `QAppManager` class manages the application lifecycle and global settings. You should create a single instance of `QAppManager` in your application.

```python
from PyQWebWindow.all import QAppManager

app = QAppManager(
    debugging=False, # Enable remote debugging (default: False)
    debugging_port=9222, # Port for remote debugging (default: 9222)
    remote_allow_origin="*", # Allowed origins for remote access (default: "*")
    disable_gpu=False, # Disable GPU hardware acceleration (default: False)
    disable_gpu_compositing=False, # Disable GPU compositing (default: False)
    theme="system", # Application theme ("system", "dark", "light") (default: "system")
    auto_quit=True # Automatically quit the application when the last window is closed (default: True)
)

# Run the application event loop
app.exec()

# Quit the application
app.quit()
```

You can also set the theme dynamically:

```python
app.theme = "dark" # or "light", "system"
```

## `QWebWindow`

The `QWebWindow` class represents a single webview window. It inherits from `WebViewController`, `BindingController`, and `WindowController`, providing a comprehensive set of functionalities.

```python
from PyQWebWindow.all import QWebWindow

window = QWebWindow(
    # Window options
    title="My Web Window", # Window title (default: None)
    icon="path/to/icon.png", # Window icon path (absolute or relative to caller file) (default: None)
    pos=(100, 100), # Initial window position (x, y) (default: None)
    size=(800, 600), # Initial window size (width, height) (default: None)
    minimum_size=(400, 300), # Minimum window size (default: None)
    maximum_size=(1200, 900), # Maximum window size (default: None)
    resizable=True, # Allow window resizing (default: True)
    on_top=False, # Keep window on top of others (default: False)
    hide_when_close=False, # Hide instead of closing when the close button is clicked (default: False)

    # Webview options
    background_color="#FFFFFF", # Webview background color (default: None)
    enable_clipboard=True, # Enable JavaScript access to clipboard (default: True)
    enable_javascript=True, # Enable JavaScript execution (default: True)
    enable_localstorage=True, # Enable localStorage (default: True)
    enable_webgl=True, # Enable WebGL (default: True)
    force_darkmode=False, # Force dark mode for web content (default: False)
    show_scrollbars=True # Show scrollbars in the webview (default: True)
)

# Start the window (optionally show it immediately)
window.start(show_when_ready=True)

# Access the underlying Qt widgets
qt_window = window.window # QMainWindow instance
qt_webview = window.webview # QWebEngineView instance
qt_webpage = window.webpage # QWebEnginePage instance
