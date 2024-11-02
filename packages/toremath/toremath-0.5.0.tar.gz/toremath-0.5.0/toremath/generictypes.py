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

from typing import TypeAlias, Optional

__all__ = ["Integer", "Decimal", "Complex", "Number", "Irrational", "Null"]

Integer: TypeAlias = int
Decimal: TypeAlias = float
Complex: TypeAlias = complex
Number: TypeAlias = Integer | Decimal | Complex
Irrational: TypeAlias = Number


# None types
Null: TypeAlias = Optional[None]
