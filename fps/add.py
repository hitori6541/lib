# Source: https://github.com/hitori6541/lib
# File: fps/add.py

def add(a, b, k=-1, mod=998244353):
    """c[i]=(a[i]+b[i])%mod
    k=-1なら長さmax(len(a),len(b))、k>=0ならk項（切り詰め・0埋め）。
    出力L項に対し時間・追加空間O(L)。
    """
    n = len(a); m = len(b)
    if k == -1: k = max(n, m)
    res = [0] * k
    for i in range(min(n, m, k)):
        res[i] = (a[i] + b[i]) % mod
    for i in range(m, min(n, k)):
        res[i] = a[i] % mod
    for i in range(n, min(m, k)):
        res[i] = b[i] % mod
    return res
