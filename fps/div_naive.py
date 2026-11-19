# Source: https://github.com/hitori6541/lib
# File: fps/div_naive.py

def div_naive(f, g, k=-1, mod=998244353):
    """FPS f/gの先頭k項を返す。k=-1なら元のlen(f)項。入力は変更しない。

    f, gは低次順の整数係数リスト。mod>=2、k>=-1。
    gの先頭0（modで判定）の個数をsとし、両方からx**sを除去する。
    除去後の分母定数項はmodで可逆なこと。条件違反・ゼロ分母・負次数はValueError。
    出力n項: 時間O(s + n * min(n, len(g)-s) + log mod)、追加空間O(n)。
    """
    if mod < 2:
        raise ValueError("mod must be at least 2")
    if k < -1:
        raise ValueError("k must be -1 or nonnegative")
    if not g:
        raise ValueError("g must not be empty")
    s = 0
    while s < len(g) and g[s] % mod == 0:
        s += 1
    if s == len(g):
        raise ValueError("g must not be zero modulo mod")
    if any(f[i] % mod != 0 for i in range(min(s, len(f)))):
        raise ValueError("f/g requires negative powers")
    inv_0 = pow(g[s], -1, mod)
    n = len(f) if k == -1 else k
    m = min(len(g) - s, n)
    h = [c % mod for c in f[s:s + n]]
    h += [0] * (n - len(h))
    gg = [c % mod for c in g[s:s + m]]
    for i in range(n):
        r = h[i]
        for j in range(1, min(m, i + 1)):
            r -= gg[j] * h[i - j]
        h[i] = r * inv_0 % mod
    return h
