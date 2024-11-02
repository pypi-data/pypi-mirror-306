from functools import lru_cache

from .function import *

__all__ = ["comb", "factorial"]


class comb(Function):
    @classmethod
    def eval(cls, n, k):
        if k < 0 or k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))


class factorial(Function):
    @classmethod
    def eval(cls, x):
        @lru_cache(maxsize=None)
        def f(x):
            return x * f(x - 1)

        if x < 0:
            return None
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result


class perm(Function):
    @classmethod
    def eval(n, k):
        """Calculate the number of k-permutations of n."""
        if k > n or k < 0:
            return 0  # If k > n or k < 0, permutations are not defined
        result = 1
        for i in range(n, n - k, -1):
            result *= i
        return result
