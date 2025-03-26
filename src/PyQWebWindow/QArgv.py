class QArgv:
    def __init__(self):
        self._key_dict = {}

    def set_key(self, key: str, value):
        self._key_dict[key] = value

    def to_list(self) -> list:
        argv = ["--webEngineArgs"]
        for key, value in self._key_dict.items():
            argv.append(f"--{key}={value}")
        return argv
