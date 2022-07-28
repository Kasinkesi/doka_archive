import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

try:
    from .. import arle
except ImportError:
    from lib.codecs.arle import arle

arle_inst = arle.Arle()


class Test_compress(unittest.TestCase):

    def test_no_input(self):
        self.assertEqual(arle_inst.compress(b''), b'')

    def test_one_symb(self):
        self.assertEqual(arle_inst.compress(b'a'), b'\x11a')

    def test_end_same(self):
        self.assertEqual(arle_inst.compress(b'abcc'), b'\x12ab\x02c')

    def test_end_diff(self):
        self.assertEqual(arle_inst.compress(b'aabc'), b'\x02a\x12bc')

    def test_run_long(self):
        self.assertEqual(arle_inst.compress(b'\x00' * 30), b'\x10\x00\x0e\x00')

    def test_run_long_diff(self):
        self.assertEqual(arle_inst.compress(b'\x00\x01' * 150),
                         b'\xff' + b'\x00\x01' * 119 + b'\x00' + b'M' + b'\x01\x00' * 30 + b'\x01')


class Test_decompress(unittest.TestCase):

    def test_no_input(self):
        self.assertEqual(arle_inst.decompress(b''), b'')

    def test_one_symb(self):
        self.assertEqual(arle_inst.decompress(b'\x11a'), b'a')

    def test_end_same(self):
        self.assertEqual(arle_inst.decompress(b'\x12ab\x02c'), b'abcc')

    def test_end_diff(self):
        self.assertEqual(arle_inst.decompress(b'\x02a\x12bc'), b'aabc')

    def test_run_long(self):
        self.assertEqual(arle_inst.decompress(b'\x10\x00\x10\x00\x10\x00\x10\x00\x06\x00'), b'\x00' * 70)

    def test_no_bytes_after_nbytes(self):
        with self.assertRaises(arle.codec.EOFError) as e:
            arle_inst.decompress(b'\x01a\x01b\x02')
        self.assertEqual("Symbol expected", e.exception.args[0])

    def test_no_bytes_after_ndifferent(self):
        with self.assertRaises(arle.codec.EOFError) as e:
            arle_inst.decompress(b'\x02a\x12b')
        self.assertEqual("Symbol expected", e.exception.args[0])


class Test_files(unittest.TestCase):

    def test_empty(self):
        arle_inst.compress_file(r'tests\data\empty.txt', r'tests\data\empty_compressed.txt')
        with open(r'tests\data\empty_compressed.txt', 'rb') as f:
            self.assertEqual(f.read(), b'\xd0arle')

    def test_compress_txt(self):
        arle_inst.compress_file(r'tests\data\txt_test.txt', r'tests\data\txt_test_compressed.txt')
        with open(r'tests\data\txt_test_compressed.txt', 'rb') as f:
            self.assertEqual(f.read(), (b'\xd0arle\x03a\x18\r\n\xd0\x91\xd0\xae\xd0\xa9'))

    def test_decompress_txt(self):
        arle_inst.decompress_file(r'tests\data\txt_test_compressed.txt', r'tests\data\txt_test_control.txt')
        with open(r'tests\data\txt_test_control.txt', 'rb') as f:
            self.assertEqual(f.read(), (b'aaa\r\n\xd0\x91\xd0\xae\xd0\xa9'))

    def test_wrong_magic(self):
        with self.assertRaises(arle.codec.MagicMismatchError) as e:
            arle_inst.decompress_file(r'tests\data\broken_bytefile.txt', '')
        self.assertEqual("Got b'Nrle\\x04' while b'\\xd0arle' was expected", e.exception.args[0])

    @classmethod
    def tearDownClass(cls):
        os.remove(r'tests\data\empty_compressed.txt')
        os.remove(r'tests\data\txt_test_compressed.txt')
        os.remove(r'tests\data\txt_test_control.txt')


if __name__ == '__main__':
    unittest.main()
