def compact(line, cnt_max=255):
    if not line:
        return ''

    cur, count = line[0], 1
    res = bytearray()

    for s in list(line[1:]) + [None]:
        if s == cur:
            if count == cnt_max:
                res.append(count)
                res.append(cur)
                count = 0
            count += 1
        else:
            res.append(count)
            res.append(cur)
            cur, count = s, 1
    return res


def decompres(line):
    count = 0
    res = bytearray()
    for s in line:
        if not count:
            count=s
        else:
            for _ in range(count):
                res.append(s)
            count = 0
    return res




if __name__ == '__main__':
    print(decompres((b'\x02A\x01B\x03A')))
    print(compact(''))
    print(compact(('A' * 700 + 'B' * 700 + 'Б').encode()))
    print(compact('AA'.encode()))
    print(compact('AAB'.encode()))
    print(compact('1'.encode()))
    print(compact('11'.encode()))
    print(compact('112'.encode()))
    print('problem')
    print(compact('0044'.encode()))                         #problen
    print(compact(('4'*202).encode()))                      #problen
    print(compact('Б'.encode()))
    print(compact('ББ'.encode()))
    print(compact('ББЮ'.encode()))
    print(compact(b'AABAAA'))
    print(compact(b'ABC'))
    print(compact(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB'))
