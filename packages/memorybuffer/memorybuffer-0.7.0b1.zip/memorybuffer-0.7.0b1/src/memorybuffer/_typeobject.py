# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('PyTypeObject',)

from ctypes import (c_long, c_ubyte, c_uint32, c_uint, c_ulong, c_ssize_t,
                    c_char_p, c_void_p, py_object, Structure, Union, sizeof)
from ._platform import py_version, is_cpython, is_pypy

# COUNT_ALLOCS = True


class PyObject(Structure):
    __slots__ = ()
    _fields_ = []
    if py_version >= (3, 12):
        class _Ob_refcnt(Union):
            _fields_ = [
            ("ob_refcnt", c_ssize_t)]
            # #if SIZEOF_VOID_P > 4
            if sizeof(c_void_p) > 4:
                _fields_.extend([
            ("ob_refcnt_split", c_uint32 * 2)])
        _anonymous_ = ("_ob_refcnt",)
        _fields_ = [
        ("_ob_refcnt", _Ob_refcnt),
        ("ob_type",    py_object),
        ]
    else:
        _fields_ = [
        ("ob_refcnt", c_ssize_t),
        ("ob_type",   py_object),
        ]
    _fields_ = tuple(_fields_)


class PyVarObject(Structure):
    __slots__ = ()
    _fields_ = [
        ("ob_base", PyObject),
        ("ob_size", c_ssize_t),  # Number of items in variable part
    ]
    _fields_ = tuple(_fields_)


class PyTypeObject(Structure):
    """Python level PyTypeObject struct analog."""

    # Equivalents of:
    #   Python-3.[8-12].x+/Include/cpython/object.h/struct _typeobject
    #   PyPy-3.[9-10].x+/pypy/module/cpyext/parse/cpyext_object.h/struct _typeobject

    # Type flags (tp_flags)
    #   (from Python-3.[8-12].x/Include/object.h and
    #   (from PyPy-3.[9-10].x/pypy/module/cpyext/include/object.h
    #
    # These flags are used to extend the type structure in a backwards-compatible
    # fashion. Extensions can use the flags to indicate (and test) when a given
    # type structure contains a new feature. The Python core will use these when
    # introducing new functionality between major revisions (to avoid mid-version
    # changes in the PYTHON_API_VERSION).
    #
    # Arbitration of the flag bit positions will need to be coordinated among
    # all extension writers who publically release their extensions (this will
    # be fewer than you might expect!)..
    #
    # Most flags were removed as of Python 3.0 to make room for new flags. (Some
    # flags are not for backwards compatibility but to indicate the presence of an
    # optional feature; these flags remain of course.)
    #
    # Type definitions should use Py_TPFLAGS_DEFAULT for their tp_flags value.
    #
    # Code can use PyType_HasFeature(type_ob, flag_value) to test whether the
    # given type object has a specified feature.

    # Py_LIMITED_API = True

    # Disallow creating instances of the type: set tp_new to NULL and don't create
    # the "__new__" key in the type dictionary.
    Py_TPFLAGS_DISALLOW_INSTANTIATION = (0x1 << 7)

    # Set if the type object is immutable: type attributes cannot be set nor deleted
    Py_TPFLAGS_IMMUTABLETYPE = (0x1 << 8)

    # Set if the type object is dynamically allocated
    Py_TPFLAGS_HEAPTYPE = (0x1 << 9)

    # Set if the type allows subclassing
    Py_TPFLAGS_BASETYPE = (0x1 << 10)

    # Set if the type is 'ready' -- fully initialized
    Py_TPFLAGS_READY = (0x1 << 12)

    # Set while the type is being 'readied', to prevent recursive ready calls
    Py_TPFLAGS_READYING = (0x1 << 13)

    # Objects support garbage collection (see objimp.h)
    Py_TPFLAGS_HAVE_GC = (0x1 << 14)

    # These two bits are preserved for Stackless Python, next after this is 17
    Py_TPFLAGS_HAVE_STACKLESS_EXTENSION = 0x0  # ifndef STACKLESS else (0x3 << 15)

    # Object has up-to-date type attribute cache
    Py_TPFLAGS_VALID_VERSION_TAG = (0x1 << 19)

    # Type is abstract and cannot be instantiated
    Py_TPFLAGS_IS_ABSTRACT = (0x1 << 20)

    # This undocumented flag gives certain built-ins their unique pattern-matching
    # behavior, which allows a single positional subpattern to match against the
    # subject itself (rather than a mapped attribute on it):
    # _Py_TPFLAGS_MATCH_SELF = (0x1 << 22)

    # Items (ob_size*tp_itemsize) are found at the end of an instance's memory
    Py_TPFLAGS_ITEMS_AT_END = (0x1 << 23)

    # These flags are used to determine if a type is a subclass.
    Py_TPFLAGS_LONG_SUBCLASS     = (0x1 << 24)
    Py_TPFLAGS_LIST_SUBCLASS     = (0x1 << 25)
    Py_TPFLAGS_TUPLE_SUBCLASS    = (0x1 << 26)
    Py_TPFLAGS_BYTES_SUBCLASS    = (0x1 << 27)
    Py_TPFLAGS_UNICODE_SUBCLASS  = (0x1 << 28)
    Py_TPFLAGS_DICT_SUBCLASS     = (0x1 << 29)
    Py_TPFLAGS_BASE_EXC_SUBCLASS = (0x1 << 30)
    Py_TPFLAGS_TYPE_SUBCLASS     = (0x1 << 31)

    if is_pypy and py_version == (3, 9):
        # These are conceptually the same as the flags above, but they are
        # PyPy-specific and are stored inside tp_pypy_flags
        Py_TPPYPYFLAGS_FLOAT_SUBCLASS = (0x1 << 0)

    # NOTE:
    # Some of the following flags reuse lower bits (removed as part of the
    # Python 3.0 transition).

    # The following flags are kept for compatibility; in previous
    # versions they indicated presence of newer tp_* fields on the
    # type struct.
    # Starting with 3.8, binary compatibility of C extensions across
    # feature releases of Python is not supported anymore (except when
    # using the stable ABI, in which all classes are created dynamically,
    # using the interpreter's memory layout.)
    # Note that older extensions using the stable ABI set these flags,
    # so the bits must not be repurposed.
    Py_TPFLAGS_HAVE_FINALIZE    = (0x1 << 0)
    Py_TPFLAGS_HAVE_VERSION_TAG = (0x1 << 18)

    # ** Default flags **
    Py_TPFLAGS_DEFAULT = Py_TPFLAGS_HAVE_STACKLESS_EXTENSION
    if py_version <= (3, 9):
        Py_TPFLAGS_DEFAULT |= Py_TPFLAGS_HAVE_VERSION_TAG

    __slots__ = ()
    _fields_ = [
        # PyObject_VAR_HEAD
        ("ob_base",           PyVarObject),
        # PyTypeObject body
        ("tp_name",           c_char_p),   # For printing, in format "<module>.<name>"
        ("tp_basicsize",      c_ssize_t),  # For allocation
        ("tp_itemsize",       c_ssize_t),  # For allocation
        # Methods to implement standard operations
        ("tp_dealloc",        c_void_p),   # destructor
        ("tp_vectorcall_offset", c_ssize_t),
        ("tp_getattr",        c_void_p),   # getattrfunc
        ("tp_setattr",        c_void_p),   # setattrfunc
        ("tp_reserved",       c_void_p),   # void*
        ("tp_repr",           c_void_p),   # reprfunc
        # Method suites for standard classes
        ("tp_as_number",      c_void_p),   # PyNumberMethods*
        ("tp_as_sequence",    c_void_p),   # PySequenceMethods*
        ("tp_as_mapping",     c_void_p),   # PyMappingMethods*
        # More standard operations (here for binary compatibility)
        ("tp_hash",           c_void_p),   # hashfunc
        ("tp_call",           c_void_p),   # ternaryfunc
        ("tp_str",            c_void_p),   # reprfunc
        ("tp_getattro",       c_void_p),   # getattrofunc
        ("tp_setattro",       c_void_p),   # setattrofunc
        # Functions to access object as input/output buffer
        ("tp_as_buffer",      c_void_p),   # PyBufferProcs*
        # Flags to define presence of optional/expanded features
        ("tp_flags",          c_ulong),
        ("tp_doc",            c_char_p),   # Documentation string
        # Assigned meaning in release 2.0
        # call function for all accessible objects
        ("tp_traverse",       c_void_p),   # traverseproc
        # delete references to contained objects
        ("tp_clear",          c_void_p),   # inquiry
        # Assigned meaning in release 2.1
        # rich comparisons
        ("tp_richcompare",    c_void_p),   # richcmpfunc
        # weak reference enabler
        ("tp_weaklistoffset", c_ssize_t),
        # Iterators
        ("tp_iter",           c_void_p),   # getiterfunc
        ("tp_iternext",       c_void_p),   # iternextfunc
        # Attribute descriptor and subclassing stuff
        ("tp_methods",        c_void_p),   # PyMethodDef*
        ("tp_members",        c_void_p),   # PyMemberDef*
        ("tp_getset",         c_void_p),   # PyGetSetDef*
        # Strong reference on a heap type, borrowed reference on a static type
        ("tp_base",           c_void_p),   # PyTypeObject*
        ("tp_dict",           py_object),
        ("tp_descr_get",      c_void_p),   # descrgetfunc
        ("tp_descr_set",      c_void_p),   # descrsetfunc
        ("tp_dictoffset",     c_ssize_t),
        ("tp_init",           c_void_p),   # initproc
        ("tp_alloc",          c_void_p),   # allocfunc
        ("tp_new",            c_void_p),   # newfunc
        ("tp_free",           c_void_p),   # freefunc # Low-level free-memory routine
        ("tp_is_gc",          c_void_p),   # inquiry  # For PyObject_IS_GC
        ("tp_bases",          py_object),
        ("tp_mro",            py_object),  # method resolution order
        ("tp_cache",          py_object),
        ("tp_subclasses",     c_void_p if py_version >= (3, 12) else py_object),
        ("tp_weaklist",       py_object),
        ("tp_del",            c_void_p),   # destructor
        # Type attribute cache version tag.
        ("tp_version_tag",    c_uint),
        ("tp_finalize",       c_void_p),   # destructor
        ("tp_vectorcall",     c_void_p)]   # vectorcallfunc
    if is_pypy and py_version == (3, 9):
        _fields_.extend([
        # bpo-37250: kept for backwards compatibility in CPython 3.8 only
        ("tp_print",          c_void_p)])
    if py_version >= (3, 12):
        _fields_.extend([
        # bitset of which type-watchers care about this type
        ("tp_watched",        c_ubyte)])   # unsigned char
    if is_pypy and py_version == (3, 9):
        # PyPy specific extra fields: make sure that they are ALWAYS at the end,
        # for compatibility with CPython
        _fields_.extend([
        # PyPy extensions
        ("tp_pypy_flags",     c_long)])
    _fields_ = tuple(_fields_)
