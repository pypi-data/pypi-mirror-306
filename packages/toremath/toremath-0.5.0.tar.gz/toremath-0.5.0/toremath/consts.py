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

from .generictypes import *

__all__ = ["calcate_const", "e", "pi", "inf", "nan", "tau"]


def calcate_const(const: str) -> Number | Irrational:
    """calculate constant value from scratch."""

    def get_e(terms=200):
        e_value = 0.0
        factorial = 1  # Start with 0! = 1
        for n in range(terms):
            if n > 0:
                factorial *= n  # Compute n! iteratively
            e_value += 1 / factorial
        return e_value

    def get_pi():
        return 3.141592653589793

    match const:
        case "e":
            return get_e()
        case "pi":
            return get_pi()
        case "inf":
            return float("inf")
        case "nan":
            return float("nan")
        case "tau":
            return 2 * get_pi()
        case _:
            raise ValueError(f"Invalid/unknown constant: {const}")


e: float = calcate_const("e")
pi: float = calcate_const("pi")
inf: float = calcate_const("inf")
nan: float = calcate_const("nan")
tau: float = calcate_const("tau")
