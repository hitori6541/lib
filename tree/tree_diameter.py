# Source: https://github.com/hitori6541/lib
# File: tree/tree_diameter.py
# submit: https://atcoder.jp/contests/abc482/submissions/80535690

class TreeDiameter:
    """重みなし無向木（n >= 1、頂点番号0..n-1）。

    add_edge()をn-1回 → build() → 必要ならbuild_forest()。
    入力が木であることは呼び出し側で保証する。
    edge_listは追加順の辺(i, j)を保持する。
    構築後は辺を追加しない。gとedge_listも直接変更しないこと。
    各構築は時間・追加空間ともにO(n)。

    build()後:
        diameter: 直径の辺数
        path: 直径の頂点列の一つ（同距離の場合の優先順位は保証しない）
        centers: 中心頂点の1要素タプル、または中心辺の両端の2要素タプル
        parent[v]: path[0]を根にした元の木の親。根は-1
        depth[v]: path[0]からの距離。根は0
        order: 同じ根からのBFS順（親が子より先）

    build_forest()後:
        偶数直径では中心頂点を除き、奇数直径では中心辺だけを除く。
        roots: 各成分の根の頂点番号
        component[v]: 成分番号i（0..len(roots)-1、その根はroots[i]）
        成分数はlen(roots)。成分番号・根の並び順は保証しない。
        forest_parent[v]: 森での親。根は-1
        forest_depth[v]: 成分の根からの距離。根は0
        forest_order: 森全体の多始点BFS順（親が子より先）
        除いた中心頂点のcomponent / forest_parent / forest_depthはすべて-1。
        forest_orderには除いた中心頂点を含めない。
        n=1ではrootsとforest_orderは空、上記3配列は[-1]。
        元の木のparent / depth / orderは保持する。
        max_depthなどの成分別集計は利用側で行う。
    """

    def __init__(self, n):
        assert n >= 1
        self.n = n
        self.g = [[] for _ in range(n)]
        self.edge_list = []
        self.built = False
        self.forest_built = False
        # build()
        self.diameter = -1
        self.path = []
        self.centers = ()
        self.parent = []
        self.depth = []
        self.order = []
        # build_forest()
        self.roots = []
        self.component = []
        self.forest_parent = []
        self.forest_depth = []
        self.forest_order = []

    def add_edge(self, i, j):
        assert not self.built
        assert 0 <= i < self.n and 0 <= j < self.n and i != j
        self.g[i].append(j)
        self.g[j].append(i)
        self.edge_list.append((i, j))

    def _bfs(self, start):
        parent = [-1] * self.n
        depth = [-1] * self.n
        depth[start] = 0
        order = [start]
        for v in order:
            for to in self.g[v]:
                if depth[to] != -1:
                    continue
                parent[to] = v
                depth[to] = depth[v] + 1
                order.append(to)
        assert len(order) == self.n
        return order, parent, depth

    def build(self):
        """BFSを2回行い直径・パス・中心と元の木の探索情報を構築。再構築は不可。"""
        assert not self.built and len(self.edge_list) == self.n - 1
        start = self._bfs(0)[0][-1]
        order, parent, depth = self._bfs(start)
        end = order[-1]
        path = []
        v = end
        while v != -1:
            path.append(v)
            v = parent[v]
        path.reverse()
        self.diameter = depth[end]
        self.path = path
        mid = self.diameter // 2
        self.centers = tuple(path[mid:mid + 1 + self.diameter % 2])
        self.parent = parent
        self.depth = depth
        self.order = order
        self.built = True

    def build_forest(self):
        """中心で分断した根付き森を多始点BFSで構築する。再構築は不可。"""
        assert self.built and not self.forest_built
        component = [-1] * self.n
        parent = [-1] * self.n
        depth = [-1] * self.n
        if len(self.centers) == 1:
            excluded = self.centers[0]
            roots = self.g[excluded][:]
        else:
            excluded = -1
            roots = list(self.centers)
        order = roots[:]
        for i, root in enumerate(roots):
            component[root] = i
            depth[root] = 0
        for v in order:
            for to in self.g[v]:
                # 中心辺の両端はともに訪問済みなので、互いに進まない。
                if to == excluded or component[to] != -1:
                    continue
                component[to] = component[v]
                parent[to] = v
                depth[to] = depth[v] + 1
                order.append(to)
        self.roots = roots
        self.component = component
        self.forest_parent = parent
        self.forest_depth = depth
        self.forest_order = order
        self.forest_built = True
