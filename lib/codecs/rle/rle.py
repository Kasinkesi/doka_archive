import io
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

try:
    from .. import codec
except ImportError:
    from lib.codecs import codec


class Rle(codec.Codec):
    def __init__(self):
        pass

    @property
    def magic(self):
        return b"\xd0rle"

    def compress_stream(self, instream, outstream):
        while True:
            line = instream.read(io.DEFAULT_BUFFER_SIZE)
            if not line:
                break
            cur, count = line[0], 1
            for s in list(line[1:]) + [None]:
                if s == cur:
                    if count == 255:
                        outstream.write(bytes([count]))
                        outstream.write(bytes([cur]))
                        count = 0
                    count += 1
                else:
                    outstream.write(bytes([count]))
                    outstream.write(bytes([cur]))
                    cur, count = s, 1

    def decompress_stream(self, instream, outstream):
        while True:
            nbytes = instream.read(1)
            if nbytes:
                nbytes = ord(nbytes)
            else:
                # expected EOF
                return

            symbol = instream.read(1)
            if symbol == b'':
                raise codec.EOFError("Symbol expected")

            outstream.write(symbol * nbytes)


# if __name__ == '__main__':
#     rle = Rle()
#     print(io.DEFAULT_BUFFER_SIZE)
#     print(rle.decompress(rle.compress(b'')))
#     print(rle.compress(('A' * 50 + 'B' * 700 + 'Б').encode()))
#     print(rle.decompress(rle.compress(('A' * 50 + 'B' * 700 + 'Б').encode())))
#     print(rle.decompress(rle.compress('AA'.encode())))
#     print(rle.decompress(rle.compress('AAB'.encode())))
#     print(rle.decompress(rle.compress('0044'.encode())))
#     print(rle.decompress(rle.compress(('4' * 202).encode())))
#     print(rle.decompress(rle.compress('Б'.encode())))
#     print(rle.decompress(rle.compress('ББ'.encode())))
#     print(rle.decompress(rle.compress('ББЮ'.encode())))
#     print(rle.decompress(rle.compress(b'AABAAA')))
#     print(rle.decompress(rle.compress(b'ABC')))
#     print(rle.decompress(rle.compress(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB')))
#     rle.compress_file('empty.txt', 'byteempty.txt')
#     rle.decompress_file('byteempty.txt', 'byteempty_control.txt')
#     rle.compress_file('filetest.txt', 'bytefile.txt')
#     rle.decompress_file('bytefile.txt', 'control.txt')
#     rle.compress_file('test.png', 'bytefile_png.txt')
#     rle.decompress_file('bytefile_png.txt', 'control.png')
#     rle.compress_file('Noize MC - Работа.mp3', 'bytefile_mp3.txt')
#     rle.decompress_file('bytefile_mp3.txt', 'control.mp3')
#     try:
#         rle.decompress_file('broken_bytefile.txt', 'broken_control.txt')
#     except MagicMismatchError as x:
#         print(x):
#         print(sys.exc_info()[0:2])
