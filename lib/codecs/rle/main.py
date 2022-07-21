class Rle:
    def __init__(self, line_length=1000):
        self.line_length = line_length

    def compres(self, array):
        if not array:
            return b''

        cur, count = array[0], 1
        comp_array = bytearray()

        for s in list(array[1:]) + [None]:
            if s == cur:
                if count == 255:
                    comp_array.append(count)
                    comp_array.append(cur)
                    count = 0
                count += 1
            else:
                comp_array.append(count)
                comp_array.append(cur)
                cur, count = s, 1
        return comp_array

    def decompres(self, byte_line):
        count = None
        res = bytearray()
        for s in byte_line:
            if not count:
                count = s
            else:
                res.extend([s]*count)
                count = None
        return res

    def archive(self, input, output):
        input = open(input, 'rb')
        output = open(output, 'wb')
        while True:
            line = input.read(self.line_length)
            if not line:
                break
            comp_line = self.compres(line)
            output.write(comp_line)
        input.close()
        output.close()

    def dearchive(self, input, output):
        '''must be even line length'''
        input = open(input, 'rb')
        output = open(output, 'wb')
        line = True
        while line:
            line = input.read(100)
            comp_line = self.decompres(line)
            output.write(comp_line)
        input.close()
        output.close()


if __name__ == '__main__':
    rle = Rle()
    print(rle.decompres(rle.compres('')))
    print(rle.compres(('A' * 700 + 'B' * 700 + 'Б').encode()))
    print(rle.decompres(rle.compres(('A' * 700 + 'B' * 700 + 'Б').encode())))
    print(rle.decompres(rle.compres('AA'.encode())))
    print(rle.decompres(rle.compres('AAB'.encode())))
    print(rle.decompres(rle.compres('1'.encode())))
    print(rle.decompres(rle.compres('11'.encode())))
    print(rle.decompres(rle.compres('112'.encode())))
    print(rle.decompres(rle.compres('0044'.encode())))
    print(rle.decompres(rle.compres(('4' * 202).encode())))
    print(rle.decompres(rle.compres('Б'.encode())))
    print(rle.decompres(rle.compres('ББ'.encode())))
    print(rle.decompres(rle.compres('ББЮ'.encode())))
    print(rle.decompres(rle.compres(b'AABAAA')))
    print(rle.decompres(rle.compres(b'ABC')))
    print(rle.decompres(rle.compres(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB')))
