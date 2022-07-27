import io
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

try:
    from .. import arle
except ImportError:
    from lib.codecs.arle import arle

arle_inst = arle.Arle()


class Test_compress_stream(unittest.TestCase):

    def setUp(self):
        self.outstream = io.BytesIO()

    def test_no_input(self):
        instream = io.BytesIO()
        arle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'')

    def test_one_symb(self):
        instream = io.BytesIO(b'a')
        arle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x11a')

    def test_end_same(self):
        instream = io.BytesIO(b'abcc')
        arle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x12ab\x02c')

    def test_end_diff(self):
        instream = io.BytesIO(b'aabc')
        arle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x02a\x12bc')

    def test_run_long(self):
        instream = io.BytesIO(b'a' * 70)
        arle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\x10a\x10a\x10a\x10a\x06a')

    def test_run_long_diff(self):
        instream = io.BytesIO(b'ab' * 200)
        arle_inst.compress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'\xff'+ b'ab'*119+b'a'+b'\xb1'+b'ba'*80+b'b')


class Test_decompress_stream(unittest.TestCase):

    def setUp(self):
        self.outstream = io.BytesIO()

    def test_no_input(self):
        instream = io.BytesIO()
        arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'')

    def test_one_symb(self):
        instream = io.BytesIO(b'\x11a')
        arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'a')

    def test_end_same(self):
        instream = io.BytesIO(b'\x12ab\x02c')
        arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'abcc')

    def test_end_diff(self):
        instream = io.BytesIO(b'\x02a\x12bc')
        arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'aabc')

    def test_run_long(self):
        instream = io.BytesIO(b'\x10a\x10a\x10a\x10a\x06a')
        arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual(self.outstream.getvalue(), b'a' * 70)

    def test_no_bytes_after_nbytes(self):
        instream = io.BytesIO(b'\x01a\x01b\x02')
        with self.assertRaises(arle.codec.EOFError) as e:
            arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual("Symbol expected", e.exception.args[0])

    def test_no_bytes_after_ndifferent(self):
        instream = io.BytesIO(b'\x02a\x12b')
        with self.assertRaises(arle.codec.EOFError) as e:
            arle_inst.decompress_stream(instream, self.outstream)
        self.assertEqual("Symbol expected", e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
