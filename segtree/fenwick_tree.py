# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/fenwicktree.py
# shakayami: https://github.com/shakayami/ACL-for-python/wiki/fenwicktree

class FenwickTree:

    n = 1; data = []
    def __init__(self, N):
        assert N >= 0
        self.n = N; self.data = [0 for _ in range(N)]
    def add(self, p, x):
        assert 0 <= p < self.n, "0 <= p < n, p={0}, n={1}".format(p, self.n)
        p += 1
        while p <= self.n:
            self.data[p - 1] += x; p += p & -p
    def sum0(self, r):
        assert 0 <= r <= self.n
        s = 0
        while r > 0:
            s += self.data[r - 1]; r -= r & -r
        return s
    def sum(self, l, r):
        assert 0<=l and l<=r and r<=self.n, "l={0},r={1},n={2}".format(l,r,self.n)
        return self.sum0(r) - self.sum0(l)
    #ここから追加分
    def max_right(self, l, f):
        """f(sum(l, r)) が True となる最大の r を返す。
        各要素は非負、f(0) == True で、区間を広げると f は高々1回 True→False に変化する。"""
        assert 0 <= l <= self.n
        assert f(0)
        if l == self.n: return self.n
        base = self.sum0(l)
        idx = acc = 0
        k = 1 << (self.n.bit_length() - 1)
        while k:
            next_idx = idx + k
            if next_idx <= self.n:
                next_acc = acc + self.data[next_idx - 1]
                if next_idx <= l or f(next_acc - base):
                    idx, acc = next_idx, next_acc
            k >>= 1
        return idx
    def min_left(self, r, f):
        """f(sum(l, r)) が True となる最小の l を返す。
        各要素は非負、f(0) == True で、区間を広げると f は高々1回 True→False に変化する。"""
        assert 0 <= r <= self.n
        assert f(0)
        if r == 0: return 0
        total = self.sum0(r)
        if f(total): return 0
        idx = acc = 0
        k = 1 << (self.n.bit_length() - 1)
        while k:
            next_idx = idx + k
            if next_idx < r:
                next_acc = acc + self.data[next_idx - 1]
                if not f(total - next_acc):
                    idx, acc = next_idx, next_acc
            k >>= 1
        return idx + 1    
    def sum_all(self): return self.sum0(self.n)
    def get(self, p): return self.sum(p, p+1)    
    def set(self, p, x): self.add(p, x-self.get(p))    
    def __repr__(self): return repr([self.get(i) for i in range(self.n)])
    def __str__(self): return self.__repr__()

class FenwickTreeMod:
    #https://github.com/shakayami/ACL-for-python/blob/master/fenwicktree.py
    #https://github.com/shakayami/ACL-for-python/wiki/fenwicktree
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

class DualFenwickTree:
    """区間加算・一点取得。区間は半開区間 [l, r) とする。"""
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

def tentou(xx):
    # 転倒数 O(|xx|log|xx|)
    rank = {x:i+1 for i,x in enumerate(sorted(set(xx)))}
    n = len(rank)
    bit = [0] * (n + 1)
    ret = 0
    for i, x in enumerate(xx):
        p = rank[x]
        le = 0
        while p:
            le += bit[p]; p -= p & -p
        ret += i - le
        p = rank[x]
        while p <= n:
            bit[p] += 1; p += p & -p
    return ret