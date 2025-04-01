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
const callbackMap = new Map()
const callbackIdFactory = () => crypto.randomUUID()
globalThis.backend._worker_finished.connect((callbackName, result) => {
    if (!callbackMap.has(callbackName)) return
    const callback = callbackMap.get(callbackName)
    callbackMap.delete(callbackName)
    callback(result)
})
for (const workerName of globalThis.backend._workers) {
    globalThis.backend[workerName] = (args, callback) => {
        const callbackName = callbackIdFactory()
        callbackMap.set(callbackName, callback)
        globalThis.backend._start_worker(workerName, callbackName, args)
    }
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
