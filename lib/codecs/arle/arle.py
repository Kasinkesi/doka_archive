# relative import:
from ..codec import *
# pycharm import:
# from lib.codecs.codec import *


class Arle(Codec):
    """ x from 2 to 254"""
    def __init__(self, x=127):
        self.x = x

    @property
    def magic(self):
        return b"arle"

    def compress_stream(self, instream, outstream):
        while True:
            line = instream.read(io.DEFAULT_BUFFER_SIZE)
            if not line:
                break
            cur, count = line[0], 1
            sub_line = bytearray()

            for s in list(line[1:]) + [None]:
                if s == cur:
                    if count == self.x:
                        outstream.write(bytes([count] + [cur]))
                        count = 0
                    elif sub_line:
                        outstream.write(bytes([count]) + sub_line)
                        count = 1
                        sub_line = bytearray()
                    count += 1
                else:
                    if count > 1 and count < self.x + 1:
                        outstream.write(bytes([count] + [cur]))
                        cur, count = s, 1
                    elif count == 255:
                        outstream.write(bytes([count]) + sub_line)
                        count = self.x + 1
                        sub_line = bytearray(bytes([cur]))
                    elif not sub_line:
                        sub_line.append(cur)
                        count = self.x + 1
                    elif sub_line:
                        sub_line.append(cur)
                        count += 1
                cur = s

            if sub_line:
                outstream.write(bytes([count]) + sub_line)

    def decompress_stream(self, instream, outstream):
        while True:
            nbytes = instream.read(1)

            if nbytes:
                nbytes = ord(nbytes)
            else:
                # expected EOF
                return

            if nbytes <= self.x:
                symbol = instream.read(1)
                if symbol == b'':
                    raise EOFError("Symbol expected")
                outstream.write(symbol * nbytes)
            elif nbytes > self.x:
                ndifferent = nbytes - self.x
                line = instream.read(ndifferent)
                if len(line) < (ndifferent):
                    raise EOFError("Symbol expected")
                outstream.write(line)


if __name__ == '__main__':
    arle = Arle()
    print(io.DEFAULT_BUFFER_SIZE)
    print(arle.decompress(arle.compress(b'')))
    print(arle.compress(('A' * 700 + 'B' * 7 + 'Б').encode()))
    print(arle.compress('Б'.encode()))
    print(arle.compress(b'ABC'))
    print(arle.decompress(arle.compress(('A' * 700 + 'B' * 700 + 'Б').encode())))
    print(arle.compress('AA'.encode()))
    print(arle.decompress(arle.compress('AA'.encode())))
    print(arle.decompress(arle.compress('AAB'.encode())))
    print(arle.decompress(arle.compress('0044'.encode())))
    print(arle.decompress(arle.compress(('4' * 202).encode())))
    print(arle.decompress(arle.compress('Б'.encode())))
    print(arle.decompress(arle.compress('ББ'.encode())))
    print(arle.decompress(arle.compress('ББЮ'.encode())))
    print(arle.decompress(arle.compress(b'AABAAA')))
    print(arle.decompress(arle.compress(b'ABC')))
    print(arle.decompress(arle.compress(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB')))
    # arle.compress_file('filetest.txt', 'bytefile.txt')
    # arle.decompress_file('bytefile.txt', 'control.txt')
    # arle.compress_file('test.png', 'bytefile_png.txt')
    # arle.decompress_file('bytefile_png.txt', 'control.png')
    # arle.compress_file('Noize MC - Работа.mp3', 'bytefile_mp3.txt')
    # arle.decompress_file('bytefile_mp3.txt', 'control.mp3')
    # try:
    #     arle.decompress_file('broken_bytefile.txt', 'broken_control.txt')
    # except MagicMismatchError as x:
    #     print(x)
    #     print(sys.exc_info()[0:2])
