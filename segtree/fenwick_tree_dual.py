# Source: https://github.com/hitori6541/lib
# File: segtree/fenwick_tree_dual.py
# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/fenwicktree.py

class DualFenwickTree:
    # 区間加算・一点取得・一点代入は各 O(log n)、初期化は O(n)。
    n = 1; data = []
    def __init__(self, N):
        assert N >= 0
        self.n = N; self.data = [0 for _ in range(N)]
    def _add(self, p, x):
        p += 1
        while p <= self.n:
            self.data[p - 1] += x; p += p & -p
    def add(self, l, r, x):
        assert 0 <= l <= r <= self.n
        if l == r: return
        self._add(l, x)
        if r < self.n: self._add(r, -x)
    def get(self, p):
        assert 0 <= p < self.n
        p += 1
        ret = 0
        while p > 0:
            ret += self.data[p - 1]; p -= p & -p
        return ret
    def set(self, p, x): self.add(p, p+1, x-self.get(p))
    def __repr__(self): return repr([self.get(i) for i in range(self.n)])
    def __str__(self): return self.__repr__()
