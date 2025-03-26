import sys
import os

def pytest_configure(config):
    """
    insert the `src` path into `sys.path`
    """
    dirname = os.path.dirname(__file__)
    src_path = os.path.join(dirname, "src")
    sys.path.insert(0, os.path.abspath(src_path))
