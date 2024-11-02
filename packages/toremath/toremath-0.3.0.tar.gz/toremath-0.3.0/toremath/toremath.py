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

from .activation import *
from .analysis import *
from .combinatorial import *
from .exponential import *
from .generalized import *
from .generictypes import *
from .logarithm import *
from .special import *
from .trig import *


class toremath:

    def __init__(self, functionName: str):
        self.function = globals().get(functionName)

    def __repr__(self):
        function_name = self.function.__name__ if callable(self.function) else "None"
        return f"tmath(function={function_name})"

    def __call__(self, *args, **kwargs):
        if callable(self.function):
            return self.function(*args, **kwargs)
        raise ValueError(f"{self.function} is not a callable function.")

tm: toremath = toremath
