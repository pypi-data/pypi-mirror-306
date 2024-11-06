# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

import sys
import platform

py_version = sys.version_info[:2]
is_cpython = (platform.python_implementation().lower() == "cpython")
is_pypy    = (platform.python_implementation().lower() == "pypy")
address    = id


def defined(varname, __getframe=sys._getframe):
    frame = __getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals


del sys, platform
