# Source: https://github.com/hitori6541/lib
# File: graph/union_find.py
# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/dsu.py

class UnionFind:
    def __init__(self, n):
        self._n = n
        self.parent_or_size = [-1] * n
    
    def unite(self, a, b):
        assert 0 <= a < self._n
        assert 0 <= b < self._n
        x, y = self.root(a), self.root(b)
        if x == y: return False
        if -self.parent_or_size[x] < -self.parent_or_size[y]: x, y = y, x
        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        return True

    def same(self, a, b):
        assert 0 <= a < self._n
        assert 0 <= b < self._n
        return self.root(a) == self.root(b)

    def root(self, a):
        assert 0 <= a < self._n
        path = []
        while self.parent_or_size[a] >= 0:
            path.append(a)
            a = self.parent_or_size[a]
        for v in path:
            self.parent_or_size[v] = a
        return a
    
    def size(self, a):
        assert 0 <= a < self._n
        return -self.parent_or_size[self.root(a)]
    
    def groups(self):
        leader_buf = [self.root(i) for i in range(self._n)]
        result = [[] for _ in range(self._n)]
        for i in range(self._n): result[leader_buf[i]].append(i)
        return [r for r in result if r != []]
    

