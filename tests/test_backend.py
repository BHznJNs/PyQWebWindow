from PyQWebWindow.controllers.Backend import Backend

def test_backend_init():
    backend = Backend()
    assert isinstance(backend._method_dict, dict)

def test_add_method():
    def test_method(): pass
    backend = Backend()
    backend.add_method(test_method)
    assert backend._method_dict["test_method"] == test_method

def test_get_method_list():
    def test_method1(): pass
    def test_method2(): pass
    backend = Backend()
    backend.add_method(test_method1)
    backend.add_method(test_method2)
    assert backend._methods == ["test_method1", "test_method2"]

def test_dispatch():
    def test_method(): return True
    def test_method_with_arg(arg: bool): return arg
    backend = Backend()
    backend.add_method(test_method)
    backend.add_method(test_method_with_arg)
    assert backend._dispatch("test_method", [])
    assert backend._dispatch("test_method_with_arg", [True])
    assert backend._dispatch("test_method_with_arg", [False]) == False
