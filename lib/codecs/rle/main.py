import io, sys


class DecodeError(Exception):
    pass


class EOFError(DecodeError):
    pass


class MalformedDataError(DecodeError):
    pass


class MagicMismatchError(MalformedDataError):
    pass


class Codec:
    def compress_stream(self, instream, outstream):
        raise NotImplementedError()

    def decompress_stream(self, instream, outstream):
        raise NotImplementedError()

    @property
    def magic(self):
        raise NotImplementedError()

    def compress(self, data):
        res = io.BytesIO()
        self.compress_stream(io.BytesIO(data), res)
        return res.getvalue()

    def decompress(self, data):
        res = io.BytesIO()
        self.decompress_stream(io.BytesIO(data), res)
        return res.getvalue()

    def compress_file(self, src, dst):
        with open(src, 'rb') as srcfile, open(dst, 'wb') as dstfile:
            dstfile.write(self.magic)
            self.compress_stream(srcfile, dstfile)

    def decompress_file(self, src, dst):
        with open(src, 'rb') as srcfile:
            header = srcfile.read(len(self.magic))
            if header != self.magic:
                raise MagicMismatchError("Got {} while {} was expected".format(header, self.magic))

            with open(dst, 'wb') as dstfile:
                self.decompress_stream(srcfile, dstfile)


class Rle(Codec):
    def __init__(self, some_parametr=1000):
        self.some_parametr = some_parametr
        self.count = None

    @property
    def magic(self):
        return b"rle"

    def compress_stream(self, instream, outstream):
        line = instream.read()
        if not line:
            return b''

        cur, count = line[0], 1
        res = bytearray()

        for s in list(line[1:]) + [None]:
            if s == cur:
                if count == 255:
                    res.append(count)
                    res.append(cur)
                    count = 0
                count += 1
            else:
                res.append(count)
                res.append(cur)
                cur, count = s, 1
        outstream.write(res)

    def decompress_stream(self, instream, outstream):
        comp_line = instream.read()
        res = bytearray()
        for s in comp_line:
            if not self.count:
                self.count = s
            else:
                res.extend([s] * self.count)
                self.count = None
        outstream.write(res)


if __name__ == '__main__':
    rle = Rle()
    print(rle.decompress(rle.compress(b'')))
    rle.compress(('A' * 700 + 'B' * 700 + 'Б').encode())
    print(rle.decompress(rle.compress(('A' * 700 + 'B' * 700 + 'Б').encode())))
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
    rle.compress_file('filetest.txt', 'bytefile.txt')
    rle.decompress_file('bytefile.txt', 'control.txt')
    rle.compress_file('test.png', 'bytefile_png.txt')
    rle.decompress_file('bytefile_png.txt', 'control.png')
    rle.compress_file('Noize MC - Работа.mp3', 'bytefile_mp3.txt')
    rle.decompress_file('bytefile_mp3.txt', 'control.mp3')
    try:
        rle.decompress_file('broken_bytefile.txt', 'broken_control.txt')
    except MagicMismatchError:
        print(sys.exc_info()[0:2])

