import math
import numpy as np
import struct
import sys

from .consts import *
from .exponential import *
from .function import *
from .generictypes import *


def cbrt(x: Number) -> Number:
    if x < 0:
        return None
    else:
        return pow(x, 1 / 3)


def ceil(num):
    # Check if the number is already an integer
    if num == int(num):
        return int(num)
    else:
        # If the number is negative, use the integer conversion directly
        # Otherwise, return the integer part plus one
        return int(num) + (1 if num > 0 else 0)


def copysign(x, y):
    return fabs(x) * (1 if y >= 0 else -1)


def degrees(x):
    return x * (180 / pi)


def dirac_delta(x, epsilon=0.01):
    """Using numpy, approximate the Dirac delta function using a Gaussian.
    for x you must use numpy.linspace()"""
    return (1 / (epsilon * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x / epsilon) ** 2)


def dist(p, q):
    # Ensure both points have the same dimension
    if len(p) != len(q):
        raise ValueError("Points must have the same dimension.")

    squared_diffs = [(x - y) ** 2 for x, y in zip(p, q)]

    return sum(squared_diffs) ** 0.5


def fabs(x):
    return x if x >= 0 else -x


def floor(x):
    if x >= 0:
        return int(x)  # For non-negative numbers, just convert to int
    else:
        return int(x) - (1 if x != int(x) else 0)  # For negative numbers


def fmod(x, y):
    if y == 0:
        raise ValueError("The divisor (y) cannot be zero.")

    result = x - (y * int(x / y))
    return result


def frexp(x):
    if x == 0.0:
        return 0.0, 0  # special case for zero
    elif x < 0.0:
        sign = -1
        x = -x  # work with positive for simplicity
    else:
        sign = 1

    exponent = 0

    # Normalize the number to [0.5, 1)
    while x >= 1.0:
        x /= 2.0
        exponent += 1
    while x < 0.5:
        x *= 2.0
        exponent -= 1

    # Return the mantissa and exponent
    return sign * x, exponent


def fsum(seq):
    total = 0.0
    c = 0.0  # A running compensation for lost low-order bits.
    for number in seq:
        y = number - c  # So far, so good: c is zero.
        t = total + y  # Alas, total is big, y small, so low-order digits of y are lost.
        c = (
            t - total
        ) - y  # (t - total) recovers the high-order part of y; subtracting y recovers the low-order part.
        total = t  # Algebraically, c should always be zero.
    return total


class gaussian(Function):
    @classmethod
    def eval(cls, x, *, mu=0, sigma=1, A=1):
        out = A

        class fraction:
            def __init__(self):
                self.top = Null
                self.low = Null

            def div(self):
                return self.top / self.low

        f = fraction()
        f.top = (x - mu) ** 2
        f.low = 2 * (sigma**2)

        return A * exp(-f.div())


def gcd(*integers):
    from functools import reduce

    def gcd_sing(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    return reduce(gcd_sing, integers)


class HeavisideStep(Function):
    @classmethod
    def eval(cls, t):
        if t < 0:
            return 0
        else:
            return 1


def hypot(x, y):
    return (x**2 + y**2) ** 0.5


def isclose(a, b, /, rel_tol=1e-09, abs_tol=0.0):
    """
    Check if two values are close to each other.
    """
    # Check if the numbers are equal
    if a == b:
        return True

    # Calculate the absolute difference
    diff = abs(a - b)

    # Calculate the absolute threshold based on the tolerances
    return diff <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def isinf(x):
    """
    Check if the given value is positive or negative infinity.
    """
    return x == float("inf") or x == float("-inf")


def isnan(x):
    """
    Check if the given value is NaN (Not a Number).
    """
    return x != x  # NaN is the only value that is not equal to itself


def isqrt(n):
    """
    Compute the integer square root of a non-negative integer.
    """
    if n < 0:
        raise ValueError("isqrt() not defined for negative values")

    # Binary search for the integer square root
    if n == 0:
        return 0
    left, right = 1, n
    while left < right:
        mid = (left + right + 1) // 2
        if mid * mid <= n:
            left = mid  # mid is a candidate
        else:
            right = mid - 1
    return left


def lcm(*integers):
    from functools import reduce

    return reduce((lambda a, b: abs(a * b) // gcd(a, b)), integers)


def ldexp(x, i):
    return x * (2**i)


def lgamma(x):
    """Compute the natural logarithm of the gamma function (lgamma) using Stirling's approximation."""
    if x <= 0:
        raise ValueError("lgamma is undefined for non-positive values.")

    # Stirling's approximation
    # lgamma(x) ≈ (x - 0.5) * log(x) - x + log(sqrt(2 * pi))
    return (x - 0.5) * math.log(x) - x + math.log(math.sqrt(2 * math.pi))


def modf(x):
    """Split x into its fractional and integer parts."""
    if x >= 0:
        integer_part = int(x)
    else:
        integer_part = int(x) - 1 if x != int(x) else int(x)

    fractional_part = x - integer_part
    return (fractional_part, float(integer_part))


def nextafter(x, y):
    """Compute the next representable floating-point number after x towards y."""
    if isnan(x) or isnan(y):
        return float("nan")
    if x == y:
        return x
    if isinf(x):
        return x  # No next after infinity in either direction

    # Get the raw bytes of the floating-point number
    (bits,) = struct.unpack("<q", struct.pack("<d", x))

    # Decide whether to move towards positive or negative direction
    if (y > x) == (x >= 0):  # Move right
        bits += 1
    else:  # Move left
        bits -= 1

    # Convert back to float
    return struct.unpack("<d", struct.pack("<q", bits))[0]


def prod(iterable):
    """Calculate the product of all elements in the iterable."""
    result = 1
    for item in iterable:
        result *= item
    return result


def radians(degrees):
    """Convert an angle from degrees to radians."""
    return degrees * (math.pi / 180)


def sqrt(x: Number) -> Number:
    if x < 0:
        return None
    else:
        return pow(x, 1 / 2)


def trunc(x):
    if x > 0:
        return int(x)  # Convert to int, discarding the decimal
    else:
        return int(x) if x == int(x) else int(x) + 1


def ulp(x):
    if x == 0.0:  # handle zero
        return sys.float_info.min  # Smallest positive normalized float

    next_float = nextafter(x, math.inf)  # Get the next representable float
    return abs(next_float - x)
