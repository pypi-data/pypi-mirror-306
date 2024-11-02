# -*- coding: utf-8 -*-

#
# ToreMath - A clone of the builtin math module
#
# Torrez Tsoi
# that1.stinkyarmpits@gmail.com
#
# License: MIT
#

from . import toremath

try:
    builtins = __import__("__builtin__")
except ImportError:
    builtins = __import__("builtins")


def install(tm="tm"):
    setattr(builtins, tm, toremath.tm)


def uninstall(tm="tm"):
    delattr(builtins, tm)
