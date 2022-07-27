import io
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

try:
    from .. import rle
except ImportError:
    from lib.codecs.rle import rle

rle_inst = rle.Rle()


class Test_compress_stream(unittest.TestCase):

    def setUp(self):
        self.outstream = io.BytesIO()

    def test_no_input(self):
        instream = io.BytesIO()
        rle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'')

    def test_one_symb(self):
        instream = io.BytesIO(b'a')
        rle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x01a')

    def test_end_same(self):
        instream = io.BytesIO(b'abcc')
        rle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x01a\x01b\x02c')

    def test_end_diff(self):
        instream = io.BytesIO(b'aabc')
        rle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x02a\x01b\x01c')

    def test_run_long(self):
        instream = io.BytesIO(b'\x00' * 700)
        rle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\xff\x00\xff\x00\xbe\x00')


class Test_decompress_stream(unittest.TestCase):

    def setUp(self):
        self.outstream = io.BytesIO()

    def test_no_input(self):
        instream = io.BytesIO()
        rle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'')

    def test_one_symb(self):
        instream = io.BytesIO(b'\x01a')
        rle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'a')

    def test_end_same(self):
        instream = io.BytesIO(b'\x01a\x01b\x02c')
        rle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'abcc')

    def test_end_diff(self):
        instream = io.BytesIO(b'\x02a\x01b\x01c')
        rle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'aabc')

    def test_run_long(self):
        instream = io.BytesIO(b'\xff\x00\xff\x00\xbe\x00')
        rle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x00' * 700)

    def test_no_bytes_after_nbytes(self):
        instream = io.BytesIO(b'\x01a\x01b\x02')
        with self.assertRaises(rle.codec.EOFError) as e:
            rle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual("Symbol expected", e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
