# Source: https://github.com/hitori6541/lib
# File: fps/mul.py

def mul(a, c, k=-1, mod=998244353):
    """b[i]=a[i]*c%modを返す。入力は変更しない。modは正整数。
    k=-1ならlen(a)項、k>=0ならk項（切り詰め・0埋め）。
    出力L項に対し時間・追加空間O(L)。
    """
    if k == -1: k = len(a)
    res = [0] * k
    c %= mod
    if c == 0: return res
    for i in range(min(len(a), k)):
        res[i] = a[i] * c % mod
    return res
