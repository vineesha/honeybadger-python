"""
Use cases:

>>> from honeybadger import honeybadger
>>> honeybadger.notify()
>>> honeybadger.configure(**kwargs)
>>> honeybadger.context(**kwargs)
"""

import sys
from .core import Honeybadger

__all__ = ['honeybadger']

honeybadger = Honeybadger()
sys.excepthook = honeybadger.exception_hook
