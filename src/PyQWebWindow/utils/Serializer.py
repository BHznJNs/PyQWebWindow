import pickle
from .Serializable import Serializable

class IpcSerializer:
    """
    The `backend` must be one of `pickle` and `json`
    """
    backend = pickle

    @staticmethod
    def dumps(obj: Serializable):
        return IpcSerializer.backend.dumps(obj)
    @staticmethod
    def loads(data: bytes):
        return IpcSerializer.backend.loads(data)
