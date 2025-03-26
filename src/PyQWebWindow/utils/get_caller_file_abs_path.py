import inspect
import os

def get_caller_file_abs_path():
    stack = inspect.stack()
    caller_frame = stack[2]
    caller_filename = caller_frame.filename
    absolute_path = os.path.abspath(caller_filename)

    del stack
    return absolute_path
