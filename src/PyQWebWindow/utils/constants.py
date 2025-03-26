INITIAL_SCRIPT = """\
const script = document.createElement("script")
script.src = "qrc:///qtwebchannel/qwebchannel.js"
script.onload = () => {
    new QWebChannel(qt.webChannelTransport, (channel) => {
        globalThis.backend = channel.objects.backend

        for (const methodName of globalThis.backend._methods) {
            globalThis.backend[methodName] = (...args) =>
                globalThis.backend._dispatch(methodName, args)
        }

        globalThis.dispatchEvent(new CustomEvent('backendloaded'))
    })
}
document.head.appendChild(script)\
"""
