# Source: https://github.com/hitori6541/lib
# File: sequence/tentou.py

def tentou(xx):
    # 転倒数 O(|xx|log|xx|)
    rank = {x:i+1 for i,x in enumerate(sorted(set(xx)))}
    n = len(rank)
    bit = [0] * (n + 1)
    ret = 0
    for i, x in enumerate(xx):
        p = rank[x]
        le = 0
        while p:
            le += bit[p]; p -= p & -p
        ret += i - le
        p = rank[x]
        while p <= n:
            bit[p] += 1; p += p & -p
    return ret
