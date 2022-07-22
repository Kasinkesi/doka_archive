class Rle:
    def __init__(self, line_length=1000, x=10):
        self.line_length = line_length
        self.x = x

    def compres(self, array):
        if not array:
            return b''

        cur, count = array[0], 1
        comp_array = bytearray()
        sub_line = bytearray()

        for s in list(array[1:]):
            if s == cur:
                if count == self.x:
                    comp_array.append(count)
                    comp_array.append(cur)
                    count = 0
                if sub_line:
                    comp_array.append(count)
                    comp_array.extend(sub_line)
                    count = 1
                    sub_line = bytearray()
                count += 1
            elif s != cur:
                if count > 1 and count < self.x+1:
                    comp_array.append(count)
                    comp_array.append(cur)
                    cur, count = s, 1
                elif count == 255:
                    comp_array.append(count)
                    comp_array.extend(sub_line)
                    count = self.x+1
                    sub_line = bytearray()              #how?
                    sub_line.append(cur)
                elif not sub_line:
                    sub_line.append(cur)
                    count = self.x+1
                elif sub_line:
                    sub_line.append(cur)
                    count += 1

            cur = s
        if sub_line:
            comp_array.append(count)
            comp_array.extend(sub_line)
            count = self.x + 1
            sub_line = bytearray()  # how?
            sub_line.append(cur)
            comp_array.append(count)
            comp_array.extend(sub_line)
        else:
            comp_array.append(count)
            comp_array.append(cur)

        return comp_array

    def decompres(self, byte_line):
        count = None
        res = bytearray()
        for s in byte_line:
            if not count:
                count = s
            else:
                if count <= self.x:
                    res.extend([s] * count)
                    count = None
                elif count>self.x+1:
                    res.append(s)
                    count-=1
                elif count == self.x+1:
                    res.append(s)
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
        """read only full file 8("""
        input = open(input, 'rb')
        output = open(output, 'wb')
        line = True
        while line:
            line = input.read()
            comp_line = self.decompres(line)
            output.write(comp_line)
        input.close()
        output.close()


if __name__ == '__main__':
    rle = Rle()
    print(rle.compres(b'AA'))
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
