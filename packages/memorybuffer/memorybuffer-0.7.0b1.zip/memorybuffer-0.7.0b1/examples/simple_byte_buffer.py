# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

import ctypes as ct
from memorybuffer import Buffer, isbuffer, Py_buffer


class ByteVector(Buffer):

    def __init__(self):
        self.vector = bytearray(b"ABCDEFGHIJ")

    # Buffer protocol

    def __getbuffer__(self, buffer: Py_buffer, flags: int):
        length   = len(self.vector)
        itemsize = 1
        buffsize = length * itemsize

        buffer.buf        = self.__from_buffer__(self.vector, buffsize)
        buffer.len        = buffsize
        buffer.itemsize   = itemsize
        buffer.readonly   = False
        buffer.ndim       = 1
        buffer.format     = b"b"  # byte
        buffer.shape      = (ct.c_ssize_t * 1)(length)
        buffer.strides    = (ct.c_ssize_t * 1)(itemsize)
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

    buf = ByteVector()

    print()
    print("Is buffer: {}".format(isbuffer(buf)))
    print()

    mem = memoryview(buf)

    for v in mem:
        print(chr(v), end="")
    print()
    print(buf.vector)
    print()

    mem[0] = ord("X")
    mem[5] = ord("Z")
    for v in mem:
        print(chr(v), end="")
    print()
    print(buf.vector)
    print()

    mem = memoryview(buf)

    for v in mem:
        print(chr(v), end="")
    print()
    print(buf.vector)
    print()

    mem[0] = ord("U")
    mem[5] = ord("V")
    for v in mem:
        print(chr(v), end="")
    print()
    print(buf.vector)
    print()


main()
