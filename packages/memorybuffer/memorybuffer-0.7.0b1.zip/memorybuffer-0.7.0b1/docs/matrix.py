
import array
import ctypes as ct
from memorybuffer import Buffer, Py_buffer


class Matrix(Buffer):

    def __init__(self, ncols: int):
        self.ncols:  int   = ncols
        self.vector: array = array.array("f")

    def add_row(self):
        """Adds a row, initially zero-filled."""
        for _ in range(self.ncols):
            self.vector.append(0.0)

    # Buffer protocol

    def __getbuffer__(self, buffer: Py_buffer, flags: int):
        length   = len(self.vector)
        itemsize = self.vector.itemsize
        buffsize = length * itemsize

        shape   = (ct.c_ssize_t * 2)()
        strides = (ct.c_ssize_t * 2)()

        shape[0] = length // self.ncols
        shape[1] = self.ncols

        # Stride 0 is the distance, in bytes, between the first elements
        # of adjacent rows.
        # Stride 1 is the distance, in bytes, between two items in a row;
        # this is the distance between two adjacent items in the vector.
        strides[0] = self.ncols * itemsize
        strides[1] = itemsize

        buffer.buf        = self.__from_buffer__(self.vector, buffsize)
        buffer.len        = buffsize  # product(shape) * itemsize
        buffer.itemsize   = itemsize
        buffer.readonly   = False
        buffer.ndim       = 2
        buffer.format     = b"f"  # float
        buffer.shape      = shape
        buffer.strides    = strides
        buffer.suboffsets = None  # for pointer arrays only
        buffer.internal   = None  # see References

    def __releasebuffer__(self, buffer: Py_buffer):
        pass
