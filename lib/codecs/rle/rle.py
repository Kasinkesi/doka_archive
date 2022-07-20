def compact(line, cnt_max=255):
    if not line:
        return ''

    i, cur, count = 1, line[0:1], 1
    res = b''

    while i <= len(line):
        s = line[i:i + 1]
        if s == cur:
            if count == cnt_max:
                res += str(count).encode() + cur
                count = 0
            count += 1
        else:
            res += str(count).encode() + cur
            cur, count = s, 1
        i += 1
    return res


if __name__ == '__main__':
    print(compact(''))
    print(compact(('A' * 700 + 'B' * 700 + 'Б').encode()))
    print(compact('AA'.encode()))
    print(compact('AAB'.encode()))
    print(compact('1'.encode()))
    print(compact('11'.encode()))
    print(compact('112'.encode()))
    print(compact('0044'.encode()))                         #problen
    print(compact(('4'*202).encode()))                      #problen
    print(compact('Б'.encode()))
    print(compact('ББ'.encode()))
    print(compact('ББЮ'.encode()))
    print(compact(b'AABAAA'))
    print(compact(b'ABC'))
    print(compact(b'AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB'))
