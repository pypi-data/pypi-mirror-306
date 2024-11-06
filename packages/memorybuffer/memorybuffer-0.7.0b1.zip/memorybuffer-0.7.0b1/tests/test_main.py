# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import array
import ctypes as ct

from memorybuffer import Py_buffer, Buffer, isbuffer


class BufferBase(Buffer):

    # Buffer protocol

    def __getbuffer__(self, buffer: Py_buffer, flags: int):
        length   = len(self.byte_buffer)
        itemsize = 1
        buffsize = length * itemsize

        buffer.buf        = self.__from_buffer__(self.byte_buffer, buffsize)
        buffer.len        = buffsize
        buffer.itemsize   = itemsize
        buffer.readonly   = self.readonly
        buffer.ndim       = 1
        buffer.format     = b"b"
        buffer.shape      = (ct.c_ssize_t * buffer.ndim)(length)
        buffer.strides    = (ct.c_ssize_t * buffer.ndim)(itemsize)
        buffer.suboffsets = None
        buffer.internal   = None

    def __releasebuffer__(self, buffer: Py_buffer):
        if self.__buffer_exports__ == 0 and buffer.buf:
            buffer.buf = None


class BytesBuffer(BufferBase):

    def __init__(self):
        self.byte_buffer = bytearray(b"ABCDEFGHIJ")
        self.readonly    = True


class CtypesCcharBuffer(BufferBase):

    def __init__(self):
        self.byte_buffer = (ct.c_char * 10)(*list(b"ABCDEFGHIJ"))
        self.readonly    = True


class CtypesCstrBuffer(BufferBase):

    def __init__(self):
        self.byte_buffer = ct.create_string_buffer(b"ABCDEFGHIJ")
        self.readonly    = True


class BytearrayBuffer(BufferBase):

    def __init__(self):
        self.byte_buffer = bytearray(b"ABCDEFGHIJ")
        self.readonly    = False


class ArrayByteBuffer(BufferBase):

    def __init__(self):
        self.byte_buffer = array.array("B", b"ABCDEFGHIJ")
        self.readonly    = False


class CtypesByteBuffer(BufferBase):

    def __init__(self):
        self.byte_buffer = (ct.c_ubyte * 10)(*list(b"ABCDEFGHIJ"))
        self.readonly    = False


class MemoryBufferTestCase(unittest.TestCase):

    def test_simple_byte_buffer(self):

        no_buf = 123
        self.assertFalse(isbuffer(no_buf))

        for ByteBuffer, expected, updated in (
            (BytesBuffer,       b"ABCDEFGHIJ",   b"XBCDEZGHIJ"),
            (CtypesCcharBuffer, b"ABCDEFGHIJ",   b"XBCDEZGHIJ"),
            (CtypesCstrBuffer,  b"ABCDEFGHIJ\0", b"XBCDEZGHIJ\0"),
            (BytearrayBuffer,   b"ABCDEFGHIJ",   b"XBCDEZGHIJ"),
            (ArrayByteBuffer,   b"ABCDEFGHIJ",   b"XBCDEZGHIJ"),
            (CtypesByteBuffer,  b"ABCDEFGHIJ",   b"XBCDEZGHIJ"),
            ):

            buf = ByteBuffer()
            self.assertTrue(isbuffer(buf))

            mem = memoryview(buf)

            self.assertSequenceEqual(bytes(mem), expected)
            self.assertSequenceEqual(bytearray(mem), bytearray(expected))
            self.assertSequenceEqual(tuple(mem), tuple(expected))
            self.assertSequenceEqual(list(mem), list(expected))

            if not buf.readonly:
                mem[0] = ord("X")
                mem[5] = ord("Z")
                self.assertSequenceEqual(bytes(mem), updated)
                self.assertSequenceEqual(bytearray(mem), bytearray(updated))
                self.assertSequenceEqual(tuple(mem), tuple(updated))
                self.assertSequenceEqual(list(mem), list(updated))
