# Source: https://github.com/hitori6541/lib
# File: fps/convolution_sparse.py

def fps_sparse_prod(f:list, g:dict, deg = -1, mod = 998244353):
    """密な係数リストfと疎な多項式gの積の先頭n項をリストで返す。

    f=[a0,a1,...]、g={指数:係数,...}。gは非空、指数は0以上の整数。
    modは正整数で、合成数も可。定数項に制約はない。
    degは-1または0以上の項数。n=deg、deg==-1ならlen(f)+max(g)。
    戻り値は長さn、係数は0以上mod未満。不足分は0埋めする。
    空のfも受け取り、長さnの0列を返す（既存仕様）。
    計算量O(n + (len(f) + 1) * len(g))、追加空間O(n)。
    fとgは変更しない。外部依存なし。
    """
    n = deg if deg != -1 else len(f) + max(g.keys())
    m = len(f)
    h = [0]*n
    for j, aj in g.items():
        for i in range(m):
            k = i+j
            if k >= n: continue
            h[k] = (h[k] + f[i] * aj) % mod
    return h
