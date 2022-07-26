# relative import:
# from ..codec import *
from lib.codecs.codec import *

class Rle(Codec):
    def __init__(self, x=150):
        self.x = x
        self.count = None

    @property
    def magic(self):
        return b"rle"

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
                        outstream.write(bytes([count]))
                        outstream.write(bytes([cur]))
                        count = 0
                    elif sub_line:
                        outstream.write(bytes([count]))
                        outstream.write(sub_line)
                        count = 1
                        sub_line = bytearray()
                    count += 1
                else:
                    if count > 1 and count < self.x + 1:
                        outstream.write(bytes([count]+[cur]))
                        # outstream.write(bytes([cur]))
                        cur, count = s, 1
                    elif count == 255:
                        outstream.write(bytes([count])+sub_line)
                        # outstream.write(sub_line)
                        count = self.x + 1
                        sub_line = bytearray()  # how?
                        sub_line.append(cur)
                        # sub_line = bytearray(str(cur), 'UTF-8')
                    elif not sub_line:
                        sub_line.append(cur)
                        count = self.x + 1
                    elif sub_line:
                        sub_line.append(cur)
                        count += 1
                cur = s

            if sub_line:
                outstream.write(bytes([count]))
                outstream.write(sub_line)

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
    rle = Rle()
    print(io.DEFAULT_BUFFER_SIZE)
    print(rle.decompress(rle.compress(b'')))
    print(rle.compress(('A' * 700 + 'B' * 7 + 'Б').encode()))
    print(rle.compress('Б'.encode()))
    print(rle.compress(b'ABC'))
    print(rle.decompress(rle.compress(('A' * 700 + 'B' * 700 + 'Б').encode())))
    print(rle.compress('AA'.encode()))
    print(rle.decompress(rle.compress('AA'.encode())))
    print(rle.decompress(rle.compress('AAB'.encode())))
    print(rle.decompress(rle.compress('0044'.encode())))
    print(rle.decompress(rle.compress(('4' * 202).encode())))
    print(rle.decompress(rle.compress('Б'.encode())))
    print(rle.decompress(rle.compress('ББ'.encode())))
    print(rle.decompress(rle.compress('ББЮ'.encode())))
    print(rle.decompress(rle.compress(b'AABAAA')))
    print(rle.decompress(rle.compress(b'ABC')))
    print(rle.decompress(rle.compress(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB')))