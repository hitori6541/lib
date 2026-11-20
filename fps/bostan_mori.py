# Source: https://github.com/hitori6541/lib
# File: fps/bostan_mori.py

from typing import Callable

# conv = NTT(998244353).convolution
def bostan_mori(P: list[int], Q: list[int], conv: Callable[[list[int], list[int]], list[int]], k: int, mod) -> int:
    """[x^k] P(x)/Q(x)。
    k >= 0、Qは非空。
    Q[0]はmodで逆元を持つこと。mod >= 2で、合成数も逆元があれば可。
    計算量O( T(m)*log(k) )
    m = max(len(P),len(Q))
    T(m)は長さO(m)の多項式の畳み込み1回の計算量。
    naiveを渡す時は↓
    conv = lambda a, b: convolution_naive(a, b, mod=10**9+7)
    bostan_mori(P, Q, conv, k, 10**9+7)
    """
    def trim(a):
        while len(a) > 1 and a[-1] == 0: a.pop()
        return a

    p = trim(P[:]); q = trim(Q[:])
    assert q[0] != 0
    if not p: return 0
    if q[0] != 1:
        q0inv = pow(q[0], -1, mod)
        q = [qi*q0inv%mod for qi in q]
        p = [pi*q0inv%mod for pi in p]
    while k:
        q1 = [-qi%mod if i%2 else qi for i,qi in enumerate(q)]
        pq = conv(p,q1)
        qq = conv(q,q1)
        p = pq[1::2] if k&1 else pq[0::2]
        if not p: return 0
        q = qq[0::2]
        k >>= 1

    return p[0]
