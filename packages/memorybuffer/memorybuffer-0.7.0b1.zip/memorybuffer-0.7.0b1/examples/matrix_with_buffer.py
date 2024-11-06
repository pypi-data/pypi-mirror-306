# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

import array
import ctypes as ct
from memorybuffer import Buffer, isbuffer, Py_buffer


class Matrix(Buffer):

    def __init__(self):
        self.ncols:  int   = 5
        self.vector: array = array.array("f", (0.0, 0.1, 0.2, 0.3, 0.4,
                                               1.0, 1.1, 1.2, 1.3, 1.4,
                                               2.0, 2.1, 2.2, 2.3, 2.4))

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
        buffer.len        = buffsize
        buffer.itemsize   = itemsize
        buffer.readonly   = False
        buffer.ndim       = 2
        buffer.format     = b"f"  # float
        buffer.shape      = shape
        buffer.strides    = strides
        buffer.suboffsets = None
        buffer.internal   = None

        print("buffer",            buffer)
        print("buffer.buf       ", ct.cast(buffer.buf, ct.POINTER(ct.c_char))[0:buffer.len])
        print("buffer.len       ", buffer.len)
        print("buffer.itemsize  ", buffer.itemsize)
        print("buffer.readonly  ", buffer.readonly)
        print("buffer.ndim      ", buffer.ndim)
        print("buffer.format    ", buffer.format)
        print("buffer.shape     ", buffer.shape[0:buffer.ndim])
        print("buffer.strides   ", buffer.strides[0:buffer.ndim])
        print("buffer.suboffsets", buffer.suboffsets._objects)
        print("buffer.internal  ", buffer.internal)
        print()

    def __releasebuffer__(self, buffer: Py_buffer):
        if self.__buffer_exports__ == 0 and buffer.buf:
            buffer.buf = None


def main():

    buf = Matrix()

    print()
    print("Is buffer: {}".format(isbuffer(buf)))
    print()

    mem = memoryview(buf)

    for row in range(mem.shape[0]):
        for col in range(mem.shape[1]):
            print(f"{mem[row,col]:4.2f}", end=" ")
        print()
    print(buf.vector)
    print()

    mem[0,0] = 11.11
    mem[1,3] = 22.22
    for row in range(mem.shape[0]):
        for col in range(mem.shape[1]):
            print(f"{mem[row,col]:4.2f}", end=" ")
        print()
    print(buf.vector)
    print()

    mem = memoryview(buf)

    for row in range(mem.shape[0]):
        for col in range(mem.shape[1]):
            print(f"{mem[row,col]:4.2f}", end=" ")
        print()
    print(buf.vector)
    print()

    mem[0,0] = 33.33
    mem[1,3] = 44.44
    for row in range(mem.shape[0]):
        for col in range(mem.shape[1]):
            print(f"{mem[row,col]:4.2f}", end=" ")
        print()
    print(buf.vector)
    print()


main()
