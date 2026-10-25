
# ---- Matrix utils (dense, mod) ----
# 使い方例:
#   C = matmul(A, B, MOD)
#   v2 = matvec(A, v, MOD)
#   Ak = matpow(A, K, MOD)
#   res = apply_pow_to_vec(A, K, [1]*N, MOD)  # = A^K * 1

from typing import List
def matmul(A: List[List[int]], B: List[List[int]], MOD: int) -> List[List[int]]:
    """NxN 行列積 (A*B) mod MOD。Bは転置して列アクセス高速化。
    O(N^3)"""
    N = len(A)
    BT = [list(col) for col in zip(*B)]
    Z = [[0]*N for _ in range(N)]
    for i in range(N):
        Ai = A[i]; Zi = Z[i]
        for j in range(N):
            s = 0
            Bj = BT[j]
            # ゼロスキップ（軽い最適化）
            for k in range(N):
                a = Ai[k]
                if a:
                    s += a * Bj[k]
            Zi[j] = s % MOD
    return Z

def matvec(A: List[List[int]], v: List[int], MOD: int) -> List[int]:
    """NxN と N ベクトルの積 (A*v) mod MOD。"""
    N = len(A)
    w = [0]*N
    for i in range(N):
        Ai = A[i]; s = 0
        for k in range(N):
            a = Ai[k]
            if a:
                s += a * v[k]
        w[i] = s % MOD
    return w

def eye(N: int) -> List[List[int]]:
    """NxN 単位行列"""
    I = [[0]*N for _ in range(N)]
    for i in range(N):
        I[i][i] = 1
    return I

def matpow(A: List[List[int]], K: int, MOD: int) -> List[List[int]]:
    """A^K mod MOD(繰り返し二乗)"""
    N = len(A)
    P = [row[:] for row in A]
    R = eye(N)
    k = K
    while k:
        if k & 1:
            R = matmul(R, P, MOD)
        k >>= 1
        if k:
            P = matmul(P, P, MOD)
    return R

def apply_pow_to_vec(A: List[List[int]], K: int, v: List[int], MOD: int) -> List[int]:
    """A^K * v を直接計算（行列×ベクトルで高速化）"""
    P = [row[:] for row in A]
    w = v[:]
    k = K
    while k:
        if k & 1:
            w = matvec(P, w, MOD)
        k >>= 1
        if k:
            P = matmul(P, P, MOD)
    return w
