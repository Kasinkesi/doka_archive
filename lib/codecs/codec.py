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