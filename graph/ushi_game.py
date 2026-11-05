# Source: https://github.com/hitori6541/lib
# File: graph/ushi_game.py
# Reference: graph/ushi_game.md

from collections import deque
from heapq import heappop, heappush
class UshiGame:
    """整数の差分制約。頂点は0始まり、追加の引数順は(j, i, c)。

    dist_*(s)はs始点の最短距離配列を返す。未到達は10**18。
    solve_*はx[t] - x[s]を最適化する。
    有限ならint、非有界なら文字列"inf" / "-inf"を返す。
    矛盾ならValueError。Dijkstraは負辺、DAG DPは閉路もValueError。
    n >= 0、頂点番号とcは適切な整数を渡すこと。
    INF = 10**18。各単純経路の重みの絶対値はINF未満を前提とする。
    """

    def __init__(self, n):
        self.n = n
        self.edges = []
        self.graph = [[] for _ in range(n)]
        self._valid = None
        self._order = None
        self._has_negative = False

    def add_le(self, j, i, c):
        """x[j] - x[i] <= cを追加。O(1)。"""
        self.edges.append((i, j, c))
        self.graph[i].append((j, c))
        self._valid = None
        self._order = None
        self._has_negative |= c < 0

    def add_lt(self, j, i, c):
        """x[j] - x[i] < cを追加（整数前提）。"""
        self.add_le(j, i, c - 1)

    def add_ge(self, j, i, c):
        """x[j] - x[i] >= cを追加。"""
        self.add_le(i, j, -c)

    def add_gt(self, j, i, c):
        """x[j] - x[i] > cを追加（整数前提）。"""
        self.add_le(i, j, -c - 1)

    def is_valid(self):
        """全体の負閉路をBellman-Fordで検出。O(N + NM)、結果を再利用。"""
        if self._valid is not None:
            return self._valid
        if not self._has_negative:
            self._valid = True
            return True
        dist = [0] * self.n
        for _ in range(self.n):
            updated = False
            for i, j, c in self.edges:
                if dist[j] > dist[i] + c:
                    dist[j] = dist[i] + c
                    updated = True
            if not updated:
                self._valid = True
                return True
        self._valid = False
        return False

    def solve_maximize(self, s, t):
        """標準はBellman-Ford版。"""
        return self.solve_maximize_bellman_ford(s, t)

    def solve_minimize(self, s, t):
        """標準はBellman-Ford版。"""
        return self.solve_minimize_bellman_ford(s, t)

    def solve_maximize_bellman_ford(self, s, t):
        dist = self.dist_bellman_ford(s)
        return "inf" if dist[t] == 10**18 else dist[t]

    def dist_bellman_ford(self, s):
        """一般グラフ用。全体の矛盾判定込みでO(N + NM)。"""
        if not self.is_valid():
            raise ValueError("inconsistent constraints")
        dist = [10**18] * self.n
        dist[s] = 0
        for _ in range(self.n - 1):
            updated = False
            for i, j, c in self.edges:
                if dist[i] == 10**18:
                    continue
                if dist[j] > dist[i] + c:
                    dist[j] = dist[i] + c
                    updated = True
            if not updated:
                break
        return dist

    def solve_minimize_bellman_ford(self, s, t):
        value = self.solve_maximize_bellman_ford(t, s)
        return "-inf" if value == "inf" else -value

    def solve_maximize_dijkstra(self, s, t):
        dist = self.dist_dijkstra(s)
        return "inf" if dist[t] == 10**18 else dist[t]

    def dist_dijkstra(self, s):
        """変換後の全辺が非負の場合のみ。O(N + M log(M + 2))。"""
        if self._has_negative:
            raise ValueError("Dijkstra requires nonnegative edges")
        # 全辺非負なら負閉路もないので、Bellman-Fordの判定は不要。
        dist = [10**18] * self.n
        dist[s] = 0
        heap = [(0, s)]
        while heap:
            d, i = heappop(heap)
            if d != dist[i]:
                continue
            for j, c in self.graph[i]:
                nd = d + c
                if dist[j] > nd:
                    dist[j] = nd
                    heappush(heap, (nd, j))
        return dist

    def solve_minimize_dijkstra(self, s, t):
        value = self.solve_maximize_dijkstra(t, s)
        return "-inf" if value == "inf" else -value

    def _topological_order(self):
        if self._order is not None:
            return self._order
        indegree = [0] * self.n
        for i, j, c in self.edges:
            indegree[j] += 1
        queue = deque(i for i in range(self.n) if indegree[i] == 0)
        order = []
        while queue:
            i = queue.popleft()
            order.append(i)
            for j, c in self.graph[i]:
                indegree[j] -= 1
                if indegree[j] == 0:
                    queue.append(j)
        if len(order) != self.n:
            raise ValueError("DAG DP requires an acyclic graph")
        self._order = order
        self._valid = True
        return order

    def solve_maximize_dag_dp(self, s, t):
        dist = self.dist_dag_dp(s)
        return "inf" if dist[t] == 10**18 else dist[t]

    def dist_dag_dp(self, s):
        """DAG用（負辺可）。全体のDAG判定込みでO(N + M)。"""
        order = self._topological_order()
        dist = [10**18] * self.n
        dist[s] = 0
        for i in order:
            if dist[i] == 10**18:
                continue
            for j, c in self.graph[i]:
                if dist[j] > dist[i] + c:
                    dist[j] = dist[i] + c
        return dist

    def solve_minimize_dag_dp(self, s, t):
        value = self.solve_maximize_dag_dp(t, s)
        return "-inf" if value == "inf" else -value
