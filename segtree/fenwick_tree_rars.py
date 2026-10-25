# Source: https://github.com/hitori6541/lib
# File: segtree/fenwick_tree_rars.py
# Adapted from shakayami's ACL-for-python with AI assistance.

class RangeAddFenwickTree:
    """
    0-indexed
    add(l, r, x): [l, r) に x を加算
    sum(l, r):    [l, r) の総和

    range add / range sum 専用高速版
    """
    __slots__ = ("n", "bit0", "bit1")

    def __init__(self, n):
        assert n >= 0
        self.n = n
        self.bit0 = [0] * (n + 1)
        self.bit1 = [0] * (n + 1)

    def add(self, l, r, x):
        assert 0 <= l <= r <= self.n
        if l == r:
            return

        n = self.n
        bit0 = self.bit0
        bit1 = self.bit1

        # D[l] += x
        # bit0 : -i * D[i]
        # bit1 :      D[i]
        i = l + 1
        x0 = -l * x
        while i <= n:
            bit0[i] += x0
            bit1[i] += x
            i += i & -i

        # D[r] -= x
        # r == n はどの query にも現れないので保持不要
        if r < n:
            i = r + 1
            x0 = r * x
            x1 = -x
            while i <= n:
                bit0[i] += x0
                bit1[i] += x1
                i += i & -i

    def sum0(self, r):
        """[0, r) の和"""
        assert 0 <= r <= self.n

        bit0 = self.bit0
        bit1 = self.bit1

        s0 = 0
        s1 = 0
        i = r
        while i:
            s0 += bit0[i]
            s1 += bit1[i]
            i -= i & -i

        return s0 + r * s1

    def sum(self, l, r):
        """[l, r) の和"""
        assert 0 <= l <= r <= self.n

        bit0 = self.bit0
        bit1 = self.bit1

        s0 = 0
        s1 = 0
        i = r
        while i:
            s0 += bit0[i]
            s1 += bit1[i]
            i -= i & -i
        sr = s0 + r * s1

        s0 = 0
        s1 = 0
        i = l
        while i:
            s0 += bit0[i]
            s1 += bit1[i]
            i -= i & -i
        sl = s0 + l * s1

        return sr - sl

    def get(self, p):
        """a[p]"""
        assert 0 <= p < self.n

        # a[p] = sum_{i=0}^p D[i]
        bit1 = self.bit1
        s = 0
        i = p + 1
        while i:
            s += bit1[i]
            i -= i & -i
        return s

    def set(self, p, x):
        assert 0 <= p < self.n
        self.add(p, p + 1, x - self.get(p))

    def sum_all(self):
        return self.sum0(self.n)

    def __repr__(self):
        return repr([self.get(i) for i in range(self.n)])

    def __str__(self):
        return self.__repr__()