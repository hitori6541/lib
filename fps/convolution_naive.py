# Source: https://github.com/hitori6541/lib
# File: fps/convolution_naive.py

def convolution_naive(a, b, mod=998244353, k=-1):
    """出力L項に対し時間O(L + min(nm, L**2))、追加空間O(L)の畳み込み。
    整数リストa, bの通常の畳み込みを正整数modで返す。入力は変更しない。
    n=len(a), m=len(b)。kは-1または0以上の項数（最高次数ではない）。
    k==-1なら全n+m-1項、それ以外は先頭k項を返し、積の末尾以降は0埋め。
    """
    n = len(a); m = len(b)
    if not a or not b: return []
    if k == -1: k = n + m - 1
    res = [0] * k
    full = range(m)
    last_full = k - m
    for i in range(min(n, k)):
        if a[i] == 0: continue
        for j in full if i <= last_full else range(k - i):
            res[i + j] += a[i] * b[j]
            res[i + j] %= mod
    return res
