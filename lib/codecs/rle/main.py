class Rle:
    def __init__(self, cnt_max=1000):
        self.cnt_max = cnt_max

    def compres(self, array):
        if not array:
            return ''

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
                for _ in range(count):
                    res.append(s)
                count = None
        return res


if __name__ == '__main__':
    rle = Rle()
    print(rle.decompres(rle.compres('')))
    print(rle.decompres(rle.compres(('A' * 700 + 'B' * 700 + 'Б').encode())))
    print(rle.decompres(rle.compres('AA'.encode())))
    print(rle.decompres(rle.compres('AAB'.encode())))
    print(rle.decompres(rle.compres('1'.encode())))
    print(rle.decompres(rle.compres('11'.encode())))
    print(rle.decompres(rle.compres('112'.encode())))
    print('problem')
    print(rle.decompres(rle.compres('0044'.encode())))
    print(rle.decompres(rle.compres(('4' * 202).encode())))
    print(rle.decompres(rle.compres('Б'.encode())))
    print(rle.decompres(rle.compres('ББ'.encode())))
    print(rle.decompres(rle.compres('ББЮ'.encode())))
    print(rle.decompres(rle.compres(b'AABAAA')))
    print(rle.decompres(rle.compres(b'ABC')))
    print(rle.decompres(rle.compres(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB')))
