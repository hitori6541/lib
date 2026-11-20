# FPSメモ

> **Source:** https://github.com/hitori6541/lib  
> **File:** `fps/fps_notes.md`

## 目次

- [メモ](#メモ)
  - [通常型母関数](#通常型母関数)
  - [指数型母関数](#指数型母関数)
  - [累積和](#累積和)
- [関数と依存関係](#関数と依存関係)
- [コピーして使う例](#コピーして使う例)
- [未実装の候補](#未実装の候補)

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

両辺に $1-x$ を掛けると、この等式を確かめられる。 $n$ 箱分を掛け合わせると、

$$
(1-x)^{-n} = \sum_{i=0}^{\infty}\binom{n+i-1}{i}x^i
$$

よって、玉の分け方は $x^r$ の係数であり、次の通り。

$$
[x^r] (1-x)^{-n} = \binom{n+r-1}{r}
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

## 関数と依存関係

必要なファイルをコピーして使う。詳しい条件・計算量は各docstring、公開範囲は [CATALOG](../CATALOG.md) を参照。

| ファイル / 関数 | 用途 |
| --- | --- |
| [add.py](add.py) / `add` | 係数ごとの加算。既定の出力長は2列の長さの最大値 |
| [mul.py](mul.py) / `mul` | 係数列の定数倍。既定の出力長は入力の長さ |
| [convolution_naive.py](convolution_naive.py) / `convolution_naive` | 密な係数列の畳み込み |
| [div_naive.py](div_naive.py) / `div_naive` | 密な係数列のFPS除算。共通のx因子は自動除去 |
| [ntt.py](ntt.py) / `NTT.convolution` | 素数modで高速畳み込み |
| [div_sparse.py](div_sparse.py) / `fps_sparse_inv` | 疎な分母によるFPS除算 |
| [convolution_sparse.py](convolution_sparse.py) / `fps_sparse_prod` | 疎な多項式との積 |
| [bostan_mori.py](bostan_mori.py) / `bostan_mori` | P/Qのk次係数。畳み込みもコピーして渡す |

- 長さ指定のある関数は末尾が `k=-1, mod=998244353`。kは出力項数で、-1ではナイーブ畳み込みは積の全長、`div_naive` は元の `len(f)` 項。
- 疎な関数の `k=-1` は、積が `len(f)+max(g)`、除算が `max(g)+1` 項。gは `{指数: 係数}` の辞書。
- Bostan–Moriは `bostan_mori(P, Q, conv, k, mod)`。kは取り出す次数。
- 除算は分母定数項がmodで可逆であること。`div_naive` は共通のx因子を除去してから判定する。分子を `[1]` にすれば逆数。
- NTTの高速経路は、積の項数以上の最小の2冪zが `MOD-1` を割り切ること。998244353なら `z <= 2**23`。Bostan–Moriの中間積も同様。

## コピーして使う例

各コメントに示したファイルを先にコピーする。

```python
# Source: https://github.com/hitori6541/lib
# File: fps/fps_notes.md

# add.py: 長さが異なる係数列の加算
assert add([1, 2], [3, 4, 5]) == [4, 6, 5]

# mul.py: 定数倍
assert mul([1, 2, 3], 3) == [3, 6, 9]

# div_naive.py: 逆数、共通のx因子がある除算
assert div_naive([1], [1, -1], k=5) == [1]*5
assert div_naive([0, 0, 1, 1], [0, 1, 0, 1], k=4, mod=7) == [0, 1, 1, 6]

# div_sparse.py: 疎な分母による除算
assert fps_sparse_inv([1], {0: 1, 1: -1}, k=5) == [1]*5

# bostan_mori.py + convolution_naive.py: Fibonacci数
mod = 998244353
conv = lambda a, b: convolution_naive(a, b, mod=mod)
# conv = NTT(mod).convolution  # ntt.pyを使う場合
assert bostan_mori([0, 1], [1, mod-1, mod-1], conv, 10, mod) == 55
```

## 未実装の候補

高速なFPS除算・逆数、log、exp、整数乗、平方根、CRTによる任意mod高速畳み込み。
