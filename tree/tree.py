# Source: https://github.com/hitori6541/lib
# File: tree/tree.py
# 木DP想定の雑Tree

class Tree:
    def __init__(self,n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.edges = []

        self.par = None
        self.child = None
        self.order = None
        self.depth = None

        self.size = None

    def add_edge(self,a,b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        self.edges.append((a,b))

    def build(self, root=0):
        self.size = None
        n = self.n
        assert len(self.edges)==n-1
        assert 0 <= root < n
        g = self.adj
        par = [-1]*n
        child = [[] for _ in range(n)]
        order = [root]
        depth = [0]*n
        for v in order:
            for nv in g[v]:
                if nv != par[v]:
                    par[nv] = v
                    child[v].append(nv)
                    order.append(nv)
                    depth[nv] = 1+depth[v]
        self.par = par
        self.child = child
        self.order = order
        self.depth = depth

    def build_size(self):
        assert self.order is not None
        size = [1]*self.n
        for v in reversed(self.order[1:]):
            size[self.par[v]] += size[v]
        self.size = size