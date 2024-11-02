#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# ToreMath - A clone of the builtin math module
#
# Torrez Tsoi
# that1.stinkyarmpits@gmail.com
#
# License: MIT
#

from .check import *
from .exponential import *
from .function import *

__all__ = ["sigmoid"]


class sigmoid(Function):
    @classmethod
    def eval(cls, x):
        _c = check(x)()
        if _c.is_passed():
            return 1 / (1 + exp(-x))
