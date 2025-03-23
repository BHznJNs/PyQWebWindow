# conftest.py
import sys
import os

def pytest_configure(config):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
