# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/scc.py
class SCC:
    """
    0-indexed 有向グラフの強連結成分分解。
    非再帰Tarjan法。O(N + M)。

    add_edge(u, v) -> build()

    group_num : SCCの個数
    ids[v]    : 頂点vの所属SCC番号
    groups[k] : SCC番号kの頂点リスト

    SCC番号はトポロジカル順。
    異なるSCC間の辺 u -> v について ids[u] < ids[v]。

    build_dag() は必要な場合のみ呼び出す。
    """

    def __init__(self, n):
        self.n = n
        self.edges = []
        self.adj = [[] for _ in range(n)]
        self.group_num = 0
        self.ids = [-1] * n
        self.groups = []
        self.dag = None
        self.rdag = None
        self._built = False

    def add_edge(self, u, v):
        assert not self._built
        assert 0 <= u < self.n
        assert 0 <= v < self.n
        self.edges.append((u, v))
        self.adj[u].append(v)

    def build(self):
        n = self.n
        edges = self.edges
        m = len(edges)

        # CSR形式の隣接リスト
        start = [0] * (n + 1)
        elist = [0] * m

        for u, v in edges:
            start[u + 1] += 1
        for i in range(n):
            start[i + 1] += start[i]

        counter = start[:]
        for u, v in edges:
            elist[counter[u]] = v
            counter[u] += 1

        visited = []
        low = [0] * n
        order = [-1] * n
        ids = [0] * n
        now = 0
        group_num = 0

        # 非再帰DFS
        for root in range(n):
            if order[root] != -1:
                continue

            stack = [(root, -1, 0), (root, -1, 1)]

            while stack:
                v, par, t = stack.pop()

                if t == 1:
                    if par != -1 and order[v] != -1:
                        low[par] = min(low[par], order[v])
                        stack.pop()
                        continue

                    low[v] = now
                    order[v] = now
                    now += 1
                    visited.append(v)

                    for j in range(start[v], start[v + 1]):
                        to = elist[j]
                        if order[to] == -1:
                            stack.append((to, v, 0))
                            stack.append((to, v, 1))
                        else:
                            low[v] = min(low[v], order[to])

                else:
                    if low[v] == order[v]:
                        while True:
                            u = visited.pop()
                            order[u] = n
                            ids[u] = group_num
                            if u == v:
                                break
                        group_num += 1

                    low[par] = min(low[par], low[v])

        # トポロジカル順になるよう反転
        for v in range(n):
            ids[v] = group_num - 1 - ids[v]

        groups = [[] for _ in range(group_num)]
        for v in range(n):
            groups[ids[v]].append(v)

        self.group_num = group_num
        self.ids = ids
        self.groups = groups
        self.dag = None
        self.rdag = None
        self._built = True

    def same(self, u, v):
        assert self._built
        return self.ids[u] == self.ids[v]

    def build_dag(self):
        """
        SCCを縮約したDAGを構築する。
        多重辺と自己ループは除去する。

        dag[k]  : SCC k から出る辺の行き先
        rdag[k] : SCC k に入る辺の始点

        O(N + M) 期待時間。
        """
        assert self._built

        if self.dag is not None:
            return self.dag, self.rdag

        k = self.group_num
        dag = [[] for _ in range(k)]
        rdag = [[] for _ in range(k)]

        seen = set()
        for u, v in self.edges:
            a = self.ids[u]
            b = self.ids[v]

            if a == b or (a, b) in seen:
                continue

            seen.add((a, b))
            dag[a].append(b)
            rdag[b].append(a)

        self.dag = dag
        self.rdag = rdag
        return dag, rdag