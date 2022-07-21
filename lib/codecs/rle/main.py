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
                for _ in range(count):
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
        '''must be even line length'''
        input = open(input, 'rb')
        output = open(output, 'wb')
        while True:
            line = input.read(100)
            if not line:
                break
            comp_line = self.decompres(line)
            output.write(comp_line)
        input.close()
        output.close()
