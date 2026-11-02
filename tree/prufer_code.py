# Source: https://github.com/hitori6541/lib
# File: tree/prufer_code.py
# ref: https://info.atcoder.jp/entry/algorithm_lectures/prufer_code
# submit: https://yukicoder.me/submissions/1196599

from heapq import heapify, heappush, heappop
def prufer_encode(edeges:list[tuple[int,int]]) -> list[int]:
    # 0-indexed
    # O(NlogN)
    n = len(edeges)+1
    assert n >= 2
    g = [[] for _ in range(n)]
    deg = [0]*n
    for a, b in edeges:
        g[a].append(b)
        g[b].append(a)
        deg[a] += 1
        deg[b] += 1

    q = []
    for v in range(n):
        if deg[v] == 1:
            q.append(v)
    heapify(q)

    ret = []
    for _ in range(n-2):
        v = heappop(q)
        assert deg[v] == 1
        deg[v] -= 1
        for nv in g[v]:
            if deg[nv] > 0:
                ret.append(nv)
                deg[nv] -= 1
                if deg[nv] == 1:
                    heappush(q,nv)
    return ret

def prufer_decode(code: list[int]) -> list[tuple[int,int]]:
    # 0-indexed
    # O(NlogN)
    n = len(code)+2
    assert n >= 2
    cnt = [0]*n
    for v in code:
        cnt[v] += 1
    q = []
    for v in range(n):
        if cnt[v] == 0:
            q.append(v)
    heapify(q)

    ret = []
    for a in code:
        b = heappop(q)
        assert cnt[b] == 0
        ret.append((a,b))
        cnt[a] -= 1
        if cnt[a] == 0:
            heappush(q,a)
    ret.append((heappop(q), heappop(q)))
    return ret
