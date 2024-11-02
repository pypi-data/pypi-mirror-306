# -*- coding: utf-8 -*-

#
# ToreMath - A clone of the builtin math module
#
# Torrez Tsoi
# that1.stinkyarmpits@gmail.com
#
# License: MIT
#

from os.path import dirname, join as pjoin

from .toremath import *  # noqa
from .builtins import install, uninstall

# Import all variables in __version__.py without explicit imports.
from . import __version__

globals().update(dict((k, v) for k, v in __version__.__dict__.items()))
