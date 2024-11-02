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

import ctypes as ct


_exponential_lib = ct.CDLL("./tmath/_modules/exponential.dll")
_exponential_lib.exp.restype = ct.c_double
_exponential_lib.exp.argtypes = [ct.c_double]

_log_lib = ct.CDLL("./tmath/_modules/logarithm.dll")
_log_lib._ln.restype = ct.c_double
_log_lib._ln.argtypes = [ct.c_double]
_log_lib._log.restype = ct.c_double
_log_lib._log.argtypes = [ct.c_double]


_trig_lib = ct.CDLL("./tmath/_modules/trigonometry.dll")
_trig_lib._acos.restype = ct.c_double
_trig_lib._acos.argtypes = [ct.c_double]
_trig_lib._asin.restype = ct.c_double
_trig_lib._asin.argtypes = [ct.c_double]


class _Libs:
    def __init__(self) -> None:
        self.exponential = _exponential_lib
        self.logarithm = _log_lib
        self.trigonometry = _trig_lib


libs = _Libs()
