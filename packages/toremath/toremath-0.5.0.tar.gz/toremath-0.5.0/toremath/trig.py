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
from .combinatorial import *
from .function import *
from .exponential import *
from .generalized import *
from .logarithm import *

__all__ = [
    "acos",
    "acosh",
    "asin",
    "asinh",
    "atan",
    "atanh",
    "cos",
    "cosh",
    "sin",
    "sinh",
    "tan",
    "tanh",
]


class acos(Function):
    @classmethod
    def eval(cls, x):
        return libs.trigonometry._acos(x)


class acosh(Function):
    @classmethod
    def eval(cls, x):
        if x < 1:
            raise ValueError("Domain error: acosh(x) is only defined for x >= 1.")
        return ln(x + sqrt(x**2 - 1))


class asin(Function):
    @classmethod
    def eval(cls, x):
        if not cls._constraint(cls, x):
            raise ValueError(
                "Domain Error: The input value must be between -1 and 1 (inclusive)."
            )
        return libs.trigonometry._asin(x)

    def _constraint(self, x):
        return -1 <= x <= 1


class asinh(Function):
    @classmethod
    def eval(cls, x):
        return ln(x + sqrt(x**2 + 1))


class atan(Function):
    @classmethod
    def eval(cls, x):
        return libs.trigonometry._atan(x)


class atanh(Function):
    @classmethod
    def eval(cls, x):
        if not cls._constraint(cls, x):
            raise ValueError("Domain Error: The input value must be between -1 and 1.")
        return libs.trigonometry._atan(x)

    def _constraint(self, x):
        return -1 < x < 1


class cos(Function):
    @classmethod
    def eval(cls, x, terms=50):
        # Normalize angle to radians
        x %= 2 * pi  # Reduce x to [0, 2π]

        out = 0
        for n in range(terms):
            term = ((-1) ** n) * (x ** (2 * n)) / factorial(2 * n)
            out += term

        return round(out, 10)


class cosh(Function):
    @classmethod
    def eval(cls, x):
        return (exp(x) + exp(-x)) / 2


class sin(Function):
    @classmethod
    def eval(cls, x, terms=50):
        return sum(
            (-1) ** n * (x ** (2 * n + 1)) / factorial(2 * n + 1) for n in range(terms)
        )


class sinh(Function):
    @classmethod
    def eval(cls, x, terms=50):
        return sum((x ** (2 * n + 1)) / factorial(2 * n + 1) for n in range(terms))


class tan(Function):
    @classmethod
    def eval(cls, x, terms=50):
        cos_x = cos(x, terms)
        if cos_x == 0:
            raise ValueError("Tangent is undefined for x = pi/2 + n*pi")
        return sin(x, terms) / cos_x


class tanh(Function):
    @classmethod
    def eval(cls, x, terms=50):
        cosh_x = cosh(x, terms)
        if cosh_x == 0:
            raise ValueError("Hyperbolic tangent is undefined for this input")
        return sinh(x, terms) / cosh_x
