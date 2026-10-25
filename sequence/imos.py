# Source: https://github.com/hitori6541/lib
# File: sequence/imos.py

class Imos1D:
    def __init__(self, list_: list[int]):
        self.n = len(list_)
        self.base = list_[:]
        self.diff = [0] * (self.n + 1)
    def add(self, l: int, r: int, w: int):
        # add w to [l, r)
        assert 0 <= l <= r <= self.n
        self.diff[l] += w
        self.diff[r] -= w
    def build(self):
        cur = 0
        self.data = [0] * self.n
        for i in range(self.n):
            cur += self.diff[i]
            self.data[i] = self.base[i] + cur
        return self.data