# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('Py_buffer', 'Buffer', 'isbuffer')

from ctypes import (c_bool, c_ubyte, c_int, c_ssize_t, c_void_p, c_char_p,
                    py_object, POINTER, pointer, cast, Structure)
from ctypes import CFUNCTYPE as CFUNC
from ._typeobject import PyTypeObject
from ._platform import py_version, is_cpython, is_pypy, address

# -------------------------------------------------------------------------- #
#                               Buffer Object                                #
# -------------------------------------------------------------------------- #

class Py_buffer(Structure):
    """Python level Py_buffer struct analog."""

    # Equivalent of:
    #   Python-3.[ 8-10].x/Include/cpython/object.h/Py_buffer
    #   Python-3.[11-12].x/Include/pybuffer.h/Py_buffer

    # Maximum number of dimensions
    PyBUF_MAX_NDIM = 64 if is_cpython else 36 if is_pypy else 64
    if is_pypy:
        Py_MAX_NDIMS = PyBUF_MAX_NDIM

    # Flags for getting buffers. Keep these in sync with inspect.BufferFlags.
    PyBUF_SIMPLE         = 0x0000
    PyBUF_WRITABLE       = 0x0001
    PyBUF_WRITEABLE      = PyBUF_WRITABLE  # backwards compatible alias
    PyBUF_FORMAT         = 0x0004
    PyBUF_ND             = 0x0008
    PyBUF_STRIDES        = 0x0010 | PyBUF_ND
    PyBUF_C_CONTIGUOUS   = 0x0020 | PyBUF_STRIDES
    PyBUF_F_CONTIGUOUS   = 0x0040 | PyBUF_STRIDES
    PyBUF_ANY_CONTIGUOUS = 0x0080 | PyBUF_STRIDES
    PyBUF_INDIRECT       = 0x0100 | PyBUF_STRIDES

    PyBUF_CONTIG     = PyBUF_ND | PyBUF_WRITABLE
    PyBUF_CONTIG_RO  = PyBUF_ND

    PyBUF_STRIDED    = PyBUF_STRIDES | PyBUF_WRITABLE
    PyBUF_STRIDED_RO = PyBUF_STRIDES

    PyBUF_RECORDS    = PyBUF_STRIDES | PyBUF_WRITABLE | PyBUF_FORMAT
    PyBUF_RECORDS_RO = PyBUF_STRIDES | PyBUF_FORMAT

    PyBUF_FULL       = PyBUF_INDIRECT | PyBUF_WRITABLE | PyBUF_FORMAT
    PyBUF_FULL_RO    = PyBUF_INDIRECT | PyBUF_FORMAT

    PyBUF_READ  = 0x0100
    PyBUF_WRITE = 0x0200
    if is_pypy:
        PyBUF_SHADOW = 0x400

    __slots__ = ()
    _fields_  = [
        ("buf",        c_void_p),
        ("obj",        py_object),  # owned reference
        ("len",        c_ssize_t),
        ("itemsize",   c_ssize_t),  # This is Py_ssize_t so it can be
                                    # pointed to by strides in simple case.
        ("readonly",   c_int),
        ("ndim",       c_int),
        ("format",     c_char_p),
        ("shape",      POINTER(c_ssize_t)),
        ("strides",    POINTER(c_ssize_t)),
        ("suboffsets", POINTER(c_ssize_t)),
        ("internal",   c_void_p)]
    if is_pypy:
        _fields_.extend([
        # PyPy extensions
        ("flags",      c_int),
        ("_strides",   c_ssize_t * Py_MAX_NDIMS),
        ("_shape",     c_ssize_t * Py_MAX_NDIMS)])
        # static store for shape and strides of
        # mono-dimensional buffers.
        # ("smalltable", c_ssize_t * 2)])
    _fields_ = tuple(_fields_)

# -------------------------------------------------------------------------- #
#                               Buffer Mixin                                 #
# -------------------------------------------------------------------------- #

class Buffer:
    """Python level buffer protocol exporter."""

    @classmethod
    def __from_buffer__(cls, obj, length):
        """Shares the part of the buffer of the given Python object.

        Returns an instance of ctypes.c_void_p that shares the 'length' part
        of the buffer of the given Python object 'obj', which must support the
        buffer interface.
        """
        return cast((c_ubyte * length).from_buffer(obj), c_void_p)

class _PyBufferProcs(Structure):

    # equivalent of: Python-(3.7.0+)/Include/object.h/PyBufferProcs

    getbufferproc     = CFUNC(c_int, py_object, POINTER(Py_buffer), c_int)
    releasebufferproc = CFUNC(None,  py_object, POINTER(Py_buffer))

    __slots__ = ()
    _fields_  = [
        ("bf_getbuffer",     getbufferproc),
        ("bf_releasebuffer", releasebufferproc)]
    _fields_ = tuple(_fields_)

@_PyBufferProcs.getbufferproc
def _bf_getbuffer(self, view_p, flags):

    try:
        getbuffer = self.__getbuffer__
    except AttributeError:
        raise NotImplementedError("abstract method") from None

    try:
        self.__buffer_exports__ = getattr(self, "__buffer_exports__", 0)
        rval = getbuffer(view_p[0] if view_p else None, flags)
        self.__buffer_exports__ += 1
    except Exception as exc:
        try:
            raise exc
        except Exception:
            return -1

    if rval is not None:
        raise BufferError("__getbuffer__ method return value was not None")

    return 0

@_PyBufferProcs.releasebufferproc
def _bf_releasebuffer(self, view_p):

    releasebuffer = getattr(self, "__releasebuffer__", None)

    try:
        self.__buffer_exports__ = getattr(self, "__buffer_exports__", 0)
        if self.__buffer_exports__ > 0:
            self.__buffer_exports__ -= 1
        if releasebuffer is not None:
            releasebuffer(view_p[0] if view_p else None)
    except Exception:
        pass


_buffer_procs = _PyBufferProcs(bf_getbuffer=_bf_getbuffer,
                               bf_releasebuffer=_bf_releasebuffer)
BufferTypeObject = PyTypeObject.from_address(address(Buffer))
BufferTypeObject.tp_as_buffer = cast(pointer(_buffer_procs), c_void_p)
BufferTypeObject.tp_flags |= (PyTypeObject.Py_TPFLAGS_DEFAULT
                              | PyTypeObject.Py_TPFLAGS_BASETYPE)
del BufferTypeObject

# -------------------------------------------------------------------------- #
#                                Check Buffer                                #
# -------------------------------------------------------------------------- #

if is_cpython:
    from ctypes import pythonapi
    isbuffer = pythonapi.PyObject_CheckBuffer
    isbuffer.argtypes = [py_object]
    isbuffer.restype  = c_bool
else:
    @CFUNC(c_bool, py_object)
    def isbuffer(obj):
        # from 3.9+: Objects/abstract.c/PyObject_CheckBuffer
        TypeObj = PyTypeObject.from_address(address(type(obj)))
        tp_as_buffer = cast(TypeObj.tp_as_buffer, POINTER(_PyBufferProcs))
        return bool(tp_as_buffer) and bool(tp_as_buffer.contents.bf_getbuffer)
