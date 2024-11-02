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

from .function import *

import math


def beta_function(x, y):
    """Compute the Beta function B(x, y) using the Gamma function."""
    return math.gamma(x) * math.gamma(y) / math.gamma(x + y)


class erf(Function):
    @classmethod
    def eval(cls, x, n=10000):
        if x < 0:
            return -erf(-x, n)

        total = 0.0
        step = x / n

        for i in range(n):
            t = i * step
            total += math.exp(-(t**2)) * step

        return (2 / math.sqrt(math.pi)) * total


class erfc(Function):
    @classmethod
    def eval(cls, x, n=10000):
        return 1 - erf(x, n)


class gamma(Function):
    # Coefficients for the Lanczos approximation
    Lanczos_g = 7
    Lanczos_p = [
        676.520368121885,
        -1259.139216722402,
        771.3234287776538,
        -176.6150291498386,
        12.507343278686905,
        -0.1385710952657201,
        9.984369578019571e-6,
        1.505632735149311e-7,
    ]

    @classmethod
    def eval(cls, x):
        return cls._gamma(cls, x)

    def _gamma(self, x):
        if x < 0.5:
            # Use reflection formula: gamma(x) = pi / sin(pi*x) * gamma(1-x)
            return math.pi / (math.sin(math.pi * x) * self._gamma(1 - x))
        else:
            x -= 1
            z = 0.99999999999980993
            for i, p in enumerate(self.Lanczos_p):
                z += p / (x + i + 1)
            t = x + self.Lanczos_g + 0.5
            return math.sqrt(2 * math.pi) * (t ** (x + 0.5)) * math.exp(-t) * z
