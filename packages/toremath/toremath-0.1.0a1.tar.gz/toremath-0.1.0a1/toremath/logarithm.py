from .clibs import *
from .consts import *
from .combinatorial import *
from .function import *

__all__ = ["ln", "log"]


class ln(Function):
    @classmethod
    def eval(cls, x):
        if x <= 0:
            raise ValueError(
                "Natural logarithm of zero or negative number is not defined."
            )
        return libs.logarithm._ln(x)


class log(Function):
    @classmethod
    def eval(cls, x, base=None):
        if x <= 0:
            raise ValueError("Logarithm of zero or negative number is not defined.")

        if base is None:
            return libs.logarithm._ln(x)
        else:
            return libs.logarithm._log(x, base)


class log10(Function):
    @classmethod
    def eval(cls, x):
        return log(x, 10)


class log1p(Function):
    @classmethod
    def eval(cls, x):
        return ln(1 + x)


class log2(Function):
    @classmethod
    def eval(cls, x):
        return log(x, 2)
