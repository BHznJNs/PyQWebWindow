INITIAL_SCRIPT = """\
globalThis.backendloaded = false
"""

INITIALIZE_METHODS = """\
for (const methodName of globalThis.backend._methods) {
    globalThis.backend[methodName] = (...args) =>
        globalThis.backend._dispatch(methodName, args)
}
"""

INITIALIZE_WORKERS = """\
for (const workerName of globalThis.backend._workers) {
    globalThis.backend[workerName] = (...args) => new Promise((resolve, _) => {
        const callback = (result) => {
            globalThis.backend._worker_finished.disconnect(callback)
            resolve(result)
        }
        globalThis.backend._worker_finished.connect(callback)
        globalThis.backend._start_worker(workerName, args)
    })
}
"""

LOADED_SCRIPT = f"""\
const script = document.createElement("script")
script.src = "qrc:///qtwebchannel/qwebchannel.js"
script.onload = () => {{
    new QWebChannel(qt.webChannelTransport, (channel) => {{
        globalThis.backend = channel.objects.backend
        {INITIALIZE_METHODS}
        {INITIALIZE_WORKERS}
        globalThis.backendloaded = true
        globalThis.dispatchEvent(new CustomEvent('backendloaded'))
    }})
}}
document.head.appendChild(script)
"""
