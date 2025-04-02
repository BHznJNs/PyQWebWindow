INITIAL_SCRIPT = """\
globalThis.backendloaded = false
"""

INITIALIZE_METHODS = """\
for (const methodName of globalThis.backend._methods) {
    globalThis.backend[methodName] = (...args) =>
        globalThis.backend._dispatch(methodName, args)
}
"""

# let taskId = 0;
# const pending = {};

# function startTask() {
#     const id = taskId++;
#     return new Promise((resolve) => {
#         pending[id] = resolve;
#         backend.startTask(id); // 通知后端执行任务并传递 id
#     });
# }

# // 统一信号处理
# _task_finished.connect((id, result) => {
#     if (pending[id]) {
#         pending[id](result);
#         delete pending[id];
#     }
# });

INITIALIZE_TASKS = """\
const callbackNameFactory = () => crypto.randomUUID()
const callbackMap = new Map()
globalThis.backend._task_finished.connect((callbackName, result) => {
    const callback = callbackMap.get(callbackName)
    if (!callback) return
    callback(result)
    callbackMap.delete(callbackName)
})
for (const taskName of globalThis.backend._tasks) {
    globalThis.backend[taskName] = (...args) => new Promise((resolve, _) => {
        const callbackName = callbackNameFactory()
        callbackMap.set(callbackName, resolve)
        globalThis.backend._start_task(taskName, callbackName, args)
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
        {INITIALIZE_TASKS}
        globalThis.backendloaded = true
        globalThis.dispatchEvent(new CustomEvent('backendloaded'))
    }})
}}
document.head.appendChild(script)
"""
