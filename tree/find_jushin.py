# Source: https://github.com/hitori6541/lib
# File: tree/find_jushin.py

from collections import deque
def FindJushin(n:int, g:list[list], w:list):
    """
    n:頂点数
    g:木の隣接リスト
    w:頂点の重みのリスト 全部1は普通の木 葉だけとかはこれで調整
    https://atcoder.jp/contests/abc291/editorial/5840
    重心の頂点番号を返す O(n)
    重心が2個あるケースもこの世にはあるけど、そのうちひとつを返す
    葉が重心になるとメイン側で壊れる可能性があるので、よく考える
    頂点重心の場合1-2; 葉重心の場合1-...-n
    """
    par = [-1]*n
    order = []
    q = deque([0])
    while q:
        v = q.popleft()
        order.append(v)
        for nv in g[v]:
            if nv != par[v]:
                par[nv] = v
                q.append(nv)
    
    ww = w[:]
    s = sum(w)
    for v in reversed(order):
        if par[v] == -1:
            continue
        p = par[v]
        ww[p] += ww[v]
    
    v = 0
    while True:
        nv = -1
        mx = 0
        for child in g[v]:
            if child == par[v]:
                continue
            if ww[child] > mx:
                nv = child
                mx = ww[child]
        if mx*2 <= s:
            return v
        else:
            v = nv