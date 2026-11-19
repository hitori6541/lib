# Source: https://github.com/hitori6541/lib
# File: fps/div_sparse.py

def fps_sparse_inv(f:list, g:dict, deg = -1, mod = 998244353):
    """密な係数リストfを疎な多項式gで割り、先頭n項をリストで返す。

    f=[b0,b1,...]、g={指数:係数,...}、戻り値hはf/g mod x**n。
    gは非空、指数は0以上の整数、g[0]はmodで逆元を持つこと。
    mod >= 2。合成数modも上の逆元条件を満たせば利用できる。
    degは-1または0以上の項数。n=deg、deg==-1ならmax(g)+1（既存仕様）。
    fは必要に応じて切り詰め・0埋めされる。degは最高次数ではなく項数。
    計算量O(n * len(g) + log mod)、追加空間O(n)。
    fとgは変更しない。外部依存なし。f=[1]でgの逆数を計算できる。
    """
    assert (len(g) > 0)
    assert (0 in g and g[0] != 0)
    n = deg if deg != -1 else max(g.keys()) + 1
    h = f[:n]
    while len(h) < n: h.append(0)
    inv_0 = pow(g[0], -1, mod)
    for i in range(n):
        r = h[i]
        for d, c in g.items():
            if d == 0: continue
            deg = i - d
            if deg < 0: continue
            r = (r - c * h[deg] % mod) % mod
        r = r * inv_0 % mod
        h[i] = r
    return h
