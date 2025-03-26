from PyQWebWindow.QArgv import QArgv

def test_qargv_create():
    argv = QArgv().to_list()
    assert argv[0] == "--webEngineArgs"
