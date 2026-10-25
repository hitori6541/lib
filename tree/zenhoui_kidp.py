# Source: https://github.com/hitori6541/lib
# File: tree/zenhoui_kidp.py
# https://qiita.com/Kiri8128/items/a011c90d25911bdb3ed3
# https://atcoder.jp/contests/njpc2017/submissions/70197832

from collections import deque
class Rerooting:
    #全方位木DP O(N)
    def __init__(self, N, edges):
        assert len(edges) == N-1
        self.N = N
        self.E = edges
        g = [[] for _ in range(N)]
        par = [-1]*N
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)
        self.X = g

        #toposo
        Q = deque([0])
        toposo = []
        while Q:
            i = Q.popleft()
            toposo.append(i)
            for a in g[i]:
                if a != par[i]:
                    par[a] = i
                    Q.append(a)
        self.par = par    
        self.toposo = toposo

        self.ME = []
        self.XX0 = []
        self.TD = []
        self.XX1 = []
    
    def solve(self, unit, merge, adj_bu, adj_td, adj_fin):
        N = self.N
        X = self.X
        par = self.par
        toposo = self.toposo

        #bottom-up もらうDP
        ME = [unit] * N #ME[v]:= vの子供たちのmerge結果
        XX = [unit] * N #状態
        for i in reversed(toposo[1:]):
            XX[i] = adj_bu(ME[i], i, par[i])
            p = par[i]
            ME[p] = merge(ME[p], XX[i])
        XX[toposo[0]] = adj_fin(ME[toposo[0]], toposo[0])
        self.ME = ME # Merge before adj
        self.XX0 = XX[:] # Bottom-up after adj

        #top-down　配るDP
        TD = [unit] * N
        for i in toposo:
            ac = TD[i]
            for j in X[i]:
                if j == par[i]:
                    continue
                TD[j] = ac
                ac = merge(ac, XX[j])
            ac = unit
            for j in reversed(X[i]):
                if j == par[i]:
                    continue
                TD[j] = adj_td(merge(TD[j], ac), j, i)
                ac = merge(ac, XX[j])
                XX[j] = adj_fin(merge(ME[j], TD[j]), j)
        self.TD = TD # Top-down after adj
        self.XX1 = XX[:] # Final Result
        return XX

#### input
n = int(input())
ee = []
for _ in range(n-1):
    a, b = [int(x) for x in input().split()]
    ee.append((a-1,b-1))
dp = Rerooting(n,ee)
####

##### Settings
"""
# state
・現在の実装では[unit]*Nで初期化するのでstateはimmutableを推奨
・mutableなstateを使う場合、merge/adjは絶対に引数を破壊しないこと
# mergeは以下を満たすこと
・結合則
・unitが単位元 merge(a, unit) = a
・現在の実装では可換性も必要
# 調整adjust, mergeの結果aをdp状態に変換する
・a: state after merge, i: child, p: parent
・adj_bu(a, i, p): 頂点iから隣接頂点pへ渡す状態を作る
・adj_td(a, i, p): 頂点pから隣接頂点iへ渡す状態を作る
・adj_fin(a, i): 頂点iを根とした最終結果を作る
・adjが送信先の辺に依存しない場合等は共通化できることもある
"""
unit = 0
def merge(a, b):
    return 
def adj_bu(a, i, p):
    return 
def adj_td(a, i, p):
    return adj_bu(a, p, i)
def adj_fin(a, i):
    return adj_bu(a, i, None)
#####

res = dp.solve(unit, merge, adj_bu, adj_td, adj_fin)