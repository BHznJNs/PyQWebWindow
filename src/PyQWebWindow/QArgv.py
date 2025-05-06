class QArgv:
    _empty = object()

    def __init__(self):
        self._key_dict = {}

    def add_key(self, key: str):
        self._key_dict[key] = QArgv._empty

    def set_key(self, key: str, value):
        self._key_dict[key] = value

    def to_list(self) -> list:
        argv = ["--webEngineArgs"]
        for key, value in self._key_dict.items():
            if value is QArgv._empty:
                argv.append(f"--{key}")
            else:
                argv.append(f"--{key}={value}")
        return argv
