.. _userguide:

Users Guide
===========

Implementing the buffer protocol
================================

| Python objects can expose memory buffers to Python code by implementing
  the "buffer protocol".
| This chapter shows how to implement the protocol and make use of the
  memory managed by an extension type from NumPy.


A matrix class
--------------

The following Python code implements a matrix of floats, where the number
of columns is fixed at construction time but rows can be added dynamically.

.. code-block:: python

   # matrix.py

   import array

   class Matrix:

       def __init__(self, ncols: int):
           self.ncols:  int   = ncols
           self.vector: array = array.array("f")

       def add_row(self):
           """Adds a row, initially zero-filled."""
           for _ in range(self.ncols):
               self.vector.append(0.0)

There are no methods to do anything productive with the matrices' contents.
We could implement custom ``__getitem__``, ``__setitem__``, etc. for this,
but instead we'll use the buffer protocol to expose the matrix's data to
Python so we can use array module (or alternatively e.g. NumPy) to do useful
work.

Implementing the buffer protocol requires adding two methods,
``__getbuffer__`` and ``__releasebuffer__``, which Python handles specially.

.. literalinclude:: matrix.py
   :language: python
   :caption:

The method ``Matrix.__getbuffer__`` fills a descriptor structure, called
a ``Py_buffer``, that is defined by the Python C-API and also has its fully
compatible ctypes based implementation as ``memorybuffer.Py_buffer`` class.
It contains a pointer to the actual buffer in memory, as well as metadata
about the shape of the array and the strides (step sizes to get from one
element or row to the next).
Its ``shape`` and ``strides`` members are pointers that must point to arrays
of type and size ``ctypes.c_ssize_t[ndim]``.
These arrays have to stay alive as long as any buffer views the data.
Fortunately ctypes guarantee this, so both can be defined/created locally
in ``__getbuffer__`` method.

The code is not yet complete, but we can already compile it and test
the basic functionality.

::

    >>> from matrix import Matrix
    >>> m = Matrix(6)
    >>> m.add_row()
    >>> m.add_row()
    >>> m.vector
    array('f', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    >>> a = memoryview(m)
    >>> for col in range(m.ncols):
    >>>     a[0,col] = 1
    >>> m.vector
    array('f', [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

Now we can view the ``Matrix`` using ``memoryview``, and modify its contents
using standard ``memoryview`` operations.


Flags
-----
We skipped some input validation in the code.
The ``flags`` argument to ``__getbuffer__`` comes from ``memoryview``,
(and other clients, e.g. ``np.asarray``) and is an OR of boolean flags
that describe the kind of array that is requested.
Strictly speaking, if the flags contain ``PyBUF_ND``, ``PyBUF_SIMPLE``,
or ``PyBUF_F_CONTIGUOUS``, ``__getbuffer__`` must raise a ``BufferError``.
These macros are class attributes of ``Py_buffer`` class which can be
imported from ``memorybuffer``.

(The matrix-in-vector structure actually conforms to ``PyBUF_ND``,
but that would prohibit ``__getbuffer__`` from filling in the strides.
A single-row matrix is F-contiguous, but a larger matrix is not.)


References
----------

The buffer interface used here is set out in :PEP:`3118`,
Revising the buffer protocol.

A tutorial for using this API from C is on Jake Vanderplas's blog,
`An Introduction to the Python Buffer Protocol
<https://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/>`_.

Reference documentation is available for
`Python 3 <https://docs.python.org/3/c-api/buffer.html>`_.
