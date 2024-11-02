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

from .clibs import *
from .consts import *
from .function import *
from .generictypes import *

__all__ = ["exp", "exp2", "expm1"]


class exp(Function):
    @classmethod
    def eval(cls, x: Number) -> Number:
        return libs.exponential.exp(x)


class exp2(Function):
    @classmethod
    def eval(cls, x: Number) -> Number:
        return 2**x


class expm1(Function):
    @classmethod
    def eval(cls, x: Number) -> Number:
        return exp(x) - 1
