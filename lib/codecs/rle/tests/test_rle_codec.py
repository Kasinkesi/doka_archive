import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

try:
    from .. import rle
except ImportError:
    from lib.codecs.rle import rle

rle_inst = rle.Rle()


class Test_compress(unittest.TestCase):

    def test_no_input(self):
        self.assertEqual(rle_inst.compress(b''), b'')

    def test_one_symb(self):
        self.assertEqual(rle_inst.compress(b'a'), b'\x01a')

    def test_end_same(self):
        self.assertEqual(rle_inst.compress(b'abcc'), b'\x01a\x01b\x02c')

    def test_end_diff(self):
        self.assertEqual(rle_inst.compress(b'aabc'), b'\x02a\x01b\x01c')

    def test_run_long(self):
        self.assertEqual(rle_inst.compress(b'\x00' * 700), b'\xff\x00\xff\x00\xbe\x00')


class Test_decompress(unittest.TestCase):

    def test_no_input(self):
        self.assertEqual(rle_inst.decompress(b''), b'')

    def test_one_symb(self):
        self.assertEqual(rle_inst.decompress(b'\x01a'), b'a')

    def test_end_same(self):
        self.assertEqual(rle_inst.decompress(b'\x01a\x01b\x02c'), b'abcc')

    def test_end_diff(self):
        self.assertEqual(rle_inst.decompress(b'\x02a\x01b\x01c'), b'aabc')

    def test_run_long(self):
        self.assertEqual(rle_inst.decompress(b'\xff\x00\xff\x00\xbe\x00'), b'\x00' * 700)

    def test_no_bytes_after_nbytes(self):
        with self.assertRaises(rle.codec.EOFError) as e:
            rle_inst.decompress(b'\x01a\x01b\x02')
        self.assertEqual("Symbol expected", e.exception.args[0])


class Test_files(unittest.TestCase):

    def test_empty(self):
        rle_inst.compress_file(r'tests\data\empty.txt', r'tests\data\empty_compressed.txt')
        with open(r'tests\data\empty_compressed.txt', 'rb') as f:
            self.assertEqual(f.read(), b'\xd0rle')

    def test_compress_txt(self):
        rle_inst.compress_file(r'tests\data\txt_test.txt', r'tests\data\txt_test_compressed.txt')
        with open(r'tests\data\txt_test_compressed.txt', 'rb') as f:
            self.assertEqual(f.read(), (b'\xd0rle\x03a\x01\r\x01\n\x01\xd0\x01\x91\x01\xd0\x01\xae\x01\xd0\x01\xa9'))

    def test_decompress_txt(self):
        rle_inst.decompress_file(r'tests\data\txt_test_compressed.txt', r'tests\data\txt_test_control.txt')
        with open(r'tests\data\txt_test_control.txt', 'rb') as f:
            self.assertEqual(f.read(), (b'aaa\r\n\xd0\x91\xd0\xae\xd0\xa9'))

    def test_wrong_magic(self):
        with self.assertRaises(rle.codec.MagicMismatchError) as e:
            rle_inst.decompress_file(r'tests\data\broken_bytefile.txt', '')
        self.assertEqual("Got b'Nrle' while b'\\xd0rle' was expected", e.exception.args[0])

    @classmethod
    def tearDownClass(cls):
        os.remove(r'tests\data\empty_compressed.txt')
        os.remove(r'tests\data\txt_test_compressed.txt')
        os.remove(r'tests\data\txt_test_control.txt')


if __name__ == '__main__':
    unittest.main()
