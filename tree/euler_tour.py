# Source: https://github.com/hitori6541/lib
# File: tree/euler_tour.py

class EulerTour:
    """n >= 1、頂点番号 0..n-1 の無向木を扱う。
    入力が木であることは呼び出し側で保証する（辺数のみ検査）。
    add_edge() → build(root) → build_lca() の順で構築する。
    lca(), dist() を使わなければ build_lca() は不要。
    """
    """
    例: 6頂点・5辺。次の順で辺を追加し、根を 0 にする。
    tree = EulerTour(6)
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (3, 5)]:
        tree.add_edge(a, b)
    tree.build(0)
    et0   = [0, 1, 3, 5, 3, 1, 4, 1, 0, 2, 0]
    et1   = [0, 1, 3, 5, 4, 2]
    et2   = [0, 1, 3, 5, 5, 3, 4, 4, 1, 2, 2, 0]
    以下の配列は頂点番号 0, 1, 2, 3, 4, 5 の順。
    into0 = [0, 1, 9, 2, 6, 3]
    into1 = [0, 1, 5, 2, 4, 3]
    into2 = [0, 1, 9, 2, 6, 3]
    out0  = [10, 7, 9, 4, 6, 3]
    out1  = [6, 5, 6, 4, 5, 4]
    out2  = [11, 8, 10, 5, 7, 4]
    """

    def __init__(self, n):
        assert n >= 1
        self.n = n; self.g = [[] for _ in range(n)]; self.par = [-1] * n; self.depth = [-1] * n
        self.ee = []
        self.et0 = []   # 全辺ぶん 2N-1長
        self.et1 = []  # 行きがけのみ
        self.et2 = []  # 行きがけ+帰りがけ
        self.into0 = []
        self.into1 = []  # 行きがけのみカウント
        self.into2 = []  # 帰りがけもカウント
        self.out0 = []  # et0 で最後に v を記録した添字（右端を含む）
        self.out1 = []  # et1 で部分木の直後の位置（半開区間の右端）
        self.out2 = []  # et2 で帰りがけの v を記録した添字（右端を含む）
        # 部分木の範囲: et0[into0[v]:out0[v]+1],
        #              et1[into1[v]:out1[v]], et2[into2[v]:out2[v]+1]
        self.built = False; self.st = []; self.shift = 0; self.mask = 0; self.lca_built = False

    def add_edge(self, a, b):
        assert not self.built
        assert 0 <= a < self.n and 0 <= b < self.n
        self.g[a].append(b); self.g[b].append(a); self.ee.append((a, b))

    def build(self, i0=0):
        assert len(self.ee) == self.n - 1 and not self.built
        assert 0 <= i0 < self.n
        n = self.n; g = self.g; par = [-1] * n; depth = [-1] * n; et0 = []; et1 = []; et2 = []
        into0 = [-1] * n; into1 = [-1] * n; into2 = [-1] * n; out0 = [-1] * n; out1 = [-1] * n
        out2 = [-1] * n; par[i0] = -1; depth[i0] = 0
        # [頂点, 親, 次に見る隣接リストの添字]
        stack = [[i0, -1, 0]]
        # root に入る
        into0[i0] = len(et0); et0.append(i0); into1[i0] = len(et1); et1.append(i0)
        into2[i0] = len(et2); et2.append(i0)
        while stack:
            v, p, i = stack[-1]
            # 親を飛ばす
            while i < len(g[v]) and g[v][i] == p:
                i += 1
            stack[-1][2] = i
            if i < len(g[v]):
                # 子へ進む
                to = g[v][i]; stack[-1][2] += 1; par[to] = v; depth[to] = depth[v] + 1
                stack.append([to, v, 0])
                # 行きがけ
                into0[to] = len(et0); et0.append(to); into1[to] = len(et1); et1.append(to)
                into2[to] = len(et2); et2.append(to)
            else:
                # v から帰る
                out0[v] = len(et0) - 1; out1[v] = len(et1); out2[v] = len(et2); et2.append(v)
                stack.pop()
                # 辺を1本戻ったので親を et0 に記録
                if p != -1:
                    et0.append(p)
        self.par = par; self.depth = depth; self.et0 = et0; self.et1 = et1; self.et2 = et2
        self.into0 = into0; self.into1 = into1; self.into2 = into2; self.out0 = out0
        self.out1 = out1; self.out2 = out2; self.built = True

    def build_lca(self):
        """build() 後に呼ぶ。LCA 用 Sparse Table を時間・空間 O(N log N) で構築。"""
        assert self.built and not self.lca_built
        shift = (self.n - 1).bit_length(); depth = self.depth
        # 整数の大小が (深さ, 頂点番号) の辞書順と一致する。
        st = [[(depth[v] << shift) | v for v in self.et0]]; m = len(self.et0); half = 1
        while half * 2 <= m:
            prev = st[-1]; row = []
            for i in range(m - half * 2 + 1):
                a = prev[i]; b = prev[i + half]; row.append(a if a <= b else b)
            st.append(row); half <<= 1
        self.st = st; self.shift = shift; self.mask = (1 << shift) - 1; self.lca_built = True

    def lca(self, u, v):
        """build_lca() 後、頂点 u, v の最小共通祖先を O(1) で返す。"""
        assert self.lca_built
        assert 0 <= u < self.n and 0 <= v < self.n
        l = self.into0[u]; r = self.into0[v]
        if l > r:
            l, r = r, l
        k = (r - l + 1).bit_length() - 1; row = self.st[k]; a = row[l]; b = row[r - (1 << k) + 1]
        return (a if a <= b else b) & self.mask

    def dist(self, u, v):
        """build_lca() 後、頂点 u, v 間の距離（辺数）を O(1) で返す。"""
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]
