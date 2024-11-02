#!/usr/bin/env python
from .function import *

import math
import sympy as sp

__all__ = ["bessel", "LegendrePolynomials", "RiemannZeta"]


class bessel(Function):
    @classmethod
    def eval(cls, n, x):
        """
        Compute the Bessel function of the first kind J_n(x) using the series expansion.
        """
        sum_result = 0.0
        for k in range(100):  # Limit the number of terms in the series
            term = ((-1) ** k * (x / 2) ** (n + 2 * k)) / (
                math.factorial(k) * math.gamma(n + k + 1)
            )
            sum_result += term
        return sum_result


class LegendrePolynomials(Function):
    @classmethod
    def eval(cls, n, x):
        P0 = 1.0  # P_0(x)
        P1 = x  # P_1(x)

        if n == 0:
            return P0
        elif n == 1:
            return P1

        # Iterate to calculate P_n(x) using the previous two polynomials
        for k in range(2, n + 1):
            Pn = ((2 * k - 1) * x * P1 - (k - 1) * P0) / k
            P0, P1 = P1, Pn  # Update P0 and P1 for the next iteration

        return Pn


class RiemannZeta(Function):
    @classmethod
    def eval(cls, s):
        x = sp.symbols("x")
        return sp.zeta(x).subs(x, s)
