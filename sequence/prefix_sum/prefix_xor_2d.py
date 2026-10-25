# Source: https://github.com/hitori6541/lib
# File: sequence/prefix_sum/prefix_xor_2d.py

class PrefixXor2D:
    def __init__(self, h: int, w: int):
        assert h > 0 and w > 0
        self.h = h
        self.w = w
        self.data = [[0] * (w + 1) for _ in range(h + 1)]
        self.built = False

    def set(self, y: int, x: int, val: int):
        assert not self.built
        self.data[y + 1][x + 1] = val

    def xor(self, y: int, x: int, val: int):
        assert not self.built
        self.data[y + 1][x + 1] ^= val

    def build(self):
        assert not self.built
        data = self.data

        for y in range(1, self.h + 1):
            row = data[y]
            for x in range(1, self.w + 1):
                row[x] ^= row[x - 1]

        for y in range(1, self.h + 1):
            row = data[y]
            prev = data[y - 1]
            for x in range(1, self.w + 1):
                row[x] ^= prev[x]

        self.built = True

    def sum(self, y0: int, x0: int, y1: int, x1: int):
        assert self.built
        assert 0 <= y0 <= y1 <= self.h
        assert 0 <= x0 <= x1 <= self.w

        s = self.data
        return s[y1][x1] ^ s[y0][x1] ^ s[y1][x0] ^ s[y0][x0]

