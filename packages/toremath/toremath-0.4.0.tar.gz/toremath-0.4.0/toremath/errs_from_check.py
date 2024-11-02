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


class InvalidTypeError(TypeError):
    """Exception raised for errors in the input type."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "InvalidTypeError"
