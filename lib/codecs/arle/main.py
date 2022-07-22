class Rle:
    """ x from 2 to 254"""

    def __init__(self, line_length=1000, x=100):
        self.line_length = line_length
        self.x = x

    def compres(self, line):
        if not line:
            return b''

        cur, count = line[0], 1
        res = bytearray()
        sub_line = bytearray()

        for s in list(line[1:]) + [None]:
            if s == cur:
                if count == self.x:
                    res.append(count)
                    res.append(cur)
                    count = 0
                elif sub_line:
                    res.append(count)
                    res.extend(sub_line)
                    count = 1
                    sub_line = bytearray()
                count += 1
            else:
                if count > 1 and count < self.x + 1:
                    res.append(count)
                    res.append(cur)
                    cur, count = s, 1
                elif count == 255:
                    res.append(count)
                    res.extend(sub_line)
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
            res.append(count)
            res.extend(sub_line)

        return res

    def decompres(self, comp_line):
        count = None
        res = bytearray()
        for s in comp_line:
            if not count:
                count = s
            else:
                if count <= self.x:
                    res.extend([s] * count)
                    count = None
                elif count > self.x + 1:
                    res.append(s)
                    count -= 1
                elif count == self.x + 1:
                    res.append(s)
                    count = None
        return res

    def archive(self, input, output):
        input = open(input, 'rb')
        output = open(output, 'wb')
        line = True
        while line:
            line = input.read(self.line_length)
            comp_line = self.compres(line)
            output.write(comp_line)
        input.close()
        output.close()

    def dearchive(self, input, output):
        """read only full file 8("""
        input = open(input, 'rb')
        output = open(output, 'wb')
        comp_line = True
        while comp_line:
            comp_line = input.read()
            line = self.decompres(comp_line)
            output.write(line)
        input.close()
        output.close()


if __name__ == '__main__':
    rle = Rle()
    print(rle.compres(b'AAA'))
    print(rle.compres(b'AAAB'))
    print(rle.compres(b'ABCDE'))
    print(rle.compres(b'AABCAA'))
    print(rle.compres(('A' * 7 + 'B' * 7 + 'Б').encode()))
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
