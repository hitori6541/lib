# Source: https://github.com/hitori6541/lib
# File: graph/union_find_weighted.py

class WeightedUnionFind:
    """0 <= x < n。diff(x, y) は同じ集合の2点に対して使う。
    サイズで併合するので再帰の深さは O(log n)。通常の競プロ規模なら問題ない。
    値を0とみなす超頂点sを追加すれば、unite(s, x, v)で値を設定できる。
    """

    def __init__(self, n):
        self.par = list(range(n))
        self.size = [1] * n
        # weight[x] = potential[x] - potential[parent[x]]
        self.weight = [0] * n

    def root(self, x):
        if self.par[x] == x:
            return x
        r = self.root(self.par[x])
        self.weight[x] += self.weight[self.par[x]]
        self.par[x] = r
        return r

    def potential(self, x):
        self.root(x)
        return self.weight[x]

    def same(self, x, y):
        return self.root(x) == self.root(y)

    def diff(self, x, y):
        # sameの判定をしてから使う
        # potential[y] - potential[x]
        return self.potential(y) - self.potential(x)

    def unite(self, x, y, w):
        """
        potential[y] - potential[x] = w を追加する。
        矛盾したら False、矛盾しなければ True。
        """
        rx = self.root(x)
        ry = self.root(y)
        wx = self.potential(x)
        wy = self.potential(y)

        if rx == ry:
            return wy - wx == w

        # ry を rx の子にするとき:
        # potential[ry] - potential[rx] = potential[x] + w - potential[y]
        val = wx + w - wy

        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
            val = -val

        self.par[ry] = rx
        self.weight[ry] = val
        self.size[rx] += self.size[ry]
        return True