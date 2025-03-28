from PyQWebWindow.QArgv import QArgv

def test_qargv_init():
    argv = QArgv().to_list()
    assert argv[0] == "--webEngineArgs"

def test_set_key():
    argv = QArgv()
    argv.set_key("remote-debugging-port", 9222)
    assert argv.to_list()[1] == "--remote-debugging-port=9222"
