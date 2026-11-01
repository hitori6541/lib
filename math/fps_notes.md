# FPSメモ

> **Source:** https://github.com/hitori6541/lib  
> **File:** `math/fps_notes.md`

## 目次

- [FPSメモ](#fpsメモ)
  - [目次](#目次)
  - [メモ](#メモ)
    - [通常型母関数](#通常型母関数)
    - [指数型母関数](#指数型母関数)
    - [累積和](#累積和)
  - [関数](#関数)
    - [fps\_sparse\_inv](#fps_sparse_inv)
    - [fps\_sparse\_prod](#fps_sparse_prod)
    - [bostan\_mori](#bostan_mori)

## メモ

二項係数の和の処理（形式的べき級数）  
https://shino-sky.hateblo.jp/entry/2020/04/16/230753

ABC222-H Beautiful Binary Tree  
https://atcoder.jp/contests/abc222/editorial/2742

ABC230-H Bullion  
https://atcoder.jp/contests/abc230/editorial/3003  
> この問題は 前回 に引き続き母関数をテーマとして作られた問題です。
> 前回はかなりテクニックに寄った話を中心に書いたので、今回はテクニックよりもイメージに寄った話を書いていきましょう。

ABC422-G Balls and Boxes  
https://atcoder.jp/contests/abc422/editorial/13823  
> この問題は 母関数 あるいは 形式的冪級数(FPS) と呼ばれるテクニックへ入門するための問題です。
> この問題および解説を通じて母関数の概念について学べたら幸いです。

maspy - 形式的べき級数解説  
https://maspypy.com/category/%e5%bd%a2%e5%bc%8f%e7%9a%84%e3%81%b9%e3%81%8d%e7%b4%9a%e6%95%b0%e8%a7%a3%e8%aa%ac

37zigen - 指数型母関数入門  
https://37zigen.com/exponential-generating-function/  

### 通常型母関数

同じ玉 $r$ 個を区別する箱 $n$ 個に分ける。1箱に入る玉の個数の母関数は、

$$
1+x+x^2+\cdots = \frac{1}{1-x}
$$

両辺に $1-x$ を掛けると、この等式を確かめられる。$n$ 箱分を掛け合わせると、

$$
(1-x)^{-n} = \sum_{i=0}^{\infty}\binom{n+i-1}{i}x^i
$$

よって、$x^r$ の係数が玉の分け方の数になる。

$$
[x^r](1-x)^{-n} = \binom{n+r-1}{r}
$$

### 指数型母関数

$$
e^x = 1+x+\frac{x^2}{2!}+\cdots+\frac{x^n}{n!}+\cdots
$$

$$
A(x) = \sum_{n=0}^{\infty}\frac{a^n x^n}{n!} = e^{ax}
$$

両辺を微分すると、どちらも元の式の $a$ 倍になる。

$x^k$ の係数から $a^k$ を取り出せる。

$$
k![x^k]e^{ax} = a^k
$$

偶数次と奇数次の項は、それぞれ $\cosh(ax)$ と $\sinh(ax)$ で取り出せる。

$$
\begin{aligned}
\cosh(ax)
&= \frac{e^{ax}+e^{-ax}}{2} \\
&= 1 + \frac{a^2x^2}{2!} + \frac{a^4x^4}{4!} + \cdots \\
&= \sum_{m=0}^{\infty}\frac{a^{2m}x^{2m}}{(2m)!}
\end{aligned}
$$

$$
\begin{aligned}
\sinh(ax)
&= \frac{e^{ax}-e^{-ax}}{2} \\
&= ax + \frac{a^3x^3}{3!} + \frac{a^5x^5}{5!} + \cdots \\
&= \sum_{m=0}^{\infty}\frac{a^{2m+1}x^{2m+1}}{(2m+1)!}
\end{aligned}
$$

### 累積和

母関数を $1-x$ で割ると、係数列の累積和の母関数になる。

## 関数

### fps_sparse_inv

```python
# Source: https://github.com/hitori6541/lib
# File: math/fps_notes.md

def fps_sparse_inv(f:list, g:dict, deg = -1, mod = 998244353):
    """
    f = [b0, b1, ...] = sum(bi*x^i)
    g = {i:ai, j:aj,...} = sum(ai*x^i)  
    h = f/g = f * ginv
    gは非空、指数は0以上、g[0]はmodで逆元を持つこと
    計算量: O(n * len(g))、追加空間: O(n)
    n = deg（deg == -1 なら max(g) + 1）
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
```

### fps_sparse_prod

```python
# Source: https://github.com/hitori6541/lib
# File: math/fps_notes.md

def fps_sparse_prod(f:list, g:dict, deg = -1, mod = 998244353):
    """
    f = [a0, a1, ...]
    g = {i:ai, j:aj, ...} <-sparse
    gは非空、指数は0以上
    計算量: O(n + len(f) * len(g))、追加空間: O(n)
    n = deg（deg == -1 なら len(f) + max(g)）
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
```

### bostan_mori

```python
# Source: https://github.com/hitori6541/lib
# File: math/fps_notes.md

from typing import Callable
# conv = NTT(998244353).convolution
def bostan_mori(P: list[int], Q: list[int], k: int, conv: Callable[[list[int], list[int]], list[int]], mod: int) -> int:
    """
    get [x^k] P(x)/Q(x)
    k >= 0、PとQは非空
    Q[0]はmodで逆元を持つこと
    入力リストP、Qは変更しない
    conv(a,b) -> modでの多項式積a*b
    計算量: O((T(m) + m) * (1 + log(k+1)))、追加空間: O(m) + convの作業領域
    m = max(len(P), len(Q))、T(m) = 長さO(m)の多項式の畳み込み1回の計算量
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
```
