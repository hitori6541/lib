# Source: https://github.com/hitori6541/lib
# File: segtree/fenwick_tree_mod.py
# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/fenwicktree.py

class FenwickTreeMod:
    # mod 付きの一点加算・一点取得・一点代入・区間和は各 O(log n)、初期化は O(n)。
    n = 1
    data = [0 for _ in range(n)]
    def __init__(self, N, mod):
        assert mod > 1
        self.n = N; self.data = [0 for _ in range(N)]
        self.mod = mod
    def add(self, p, x):
        assert 0 <= p < self.n, "0 <= p < n, p={0}, n={1}".format(p, self.n)
        mod = self.mod
        x %= mod
        p += 1
        while p <= self.n:
            self.data[p-1] += x
            self.data[p-1] %= mod
            p += p & -p
    def sum0(self, r):
        assert 0 <= r <= self.n
        mod = self.mod
        s = 0
        while r > 0:
            s += self.data[r - 1]
            s %= mod
            r -= r & -r
        return s
    def sum(self, l, r):
        assert 0<=l and l<=r and r<=self.n, "l={0},r={1},n={2}".format(l,r,self.n)
        return (self.sum0(r) - self.sum0(l))%self.mod
    #ここから追加分
    def sum_all(self): return self.sum0(self.n)%self.mod
    def get(self, p): return self.sum(p, p+1)    
    def set(self, p, x): self.add(p, x-self.get(p))
    def __repr__(self): return repr([self.get(i) for i in range(self.n)])
    def __str__(self): return self.__repr__()
