from .clibs import *
from .consts import *
from .function import *
from .generictypes import *


class exp(Function):
    @classmethod
    def eval(cls, x: Number) -> Number:
        return libs.exponential.exp(x)


class exp(Function):
    @classmethod
    def eval(cls, x: Number) -> Number:
        return 2**x


class expm1(Function):
    @classmethod
    def eval(cls, x: Number) -> Number:
        return exp(x) - 1


