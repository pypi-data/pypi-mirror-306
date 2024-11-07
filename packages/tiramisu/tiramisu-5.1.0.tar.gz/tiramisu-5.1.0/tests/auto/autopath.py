"""automatically sets the PYTHONPATH before running the unit tests

This is supposed to be used in development mode (i.e. testing from a fresh
checkout)
"""

from os.path import dirname, abspath, join, normpath
import sys

def do_autopath():
    HERE = dirname(abspath(__file__))
    PATH = normpath(join(HERE, '..', '..', 'tiramisu'))
    if PATH not in sys.path:
        sys.path.insert(1, PATH)
