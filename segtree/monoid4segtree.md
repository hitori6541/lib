# Segtree モノイド集

## 目次

- [Sum and prefix minimum](#sum-and-prefix-minimum)
- [Tropical min-plus](#tropical-min-plus)
- [Bitwise matrix](#bitwise-matrix)

## Sum and prefix minimum

```python
# (sum, acc_min)
c = [1,-1]
e = (0,0)
def op(a, b): return (a[0]+b[0], min(a[1], a[0]+b[1]))
```

## Tropical min-plus

```python
"""
トロピカル min-plus
https://atcoder.jp/contests/abc456/submissions/75478403
x:払ってない
o:払った
(x->x, x->o, o->x, o->o)
行列の要素の並べ方がなんか変かもだけど、中身は合ってるっぽい
"""
inf = 10**18
def op(x, y):
    x_xx, x_xo, x_ox, x_oo = x
    y_xx, y_xo, y_ox, y_oo = y
    z_xx = min(x_xx + y_xx, x_xo + y_ox)
    z_xo = min(x_xx + y_xo, x_xo + y_oo)
    z_ox = min(x_ox + y_xx, x_oo + y_ox)
    z_oo = min(x_ox + y_xo, x_oo + y_oo)
    return (z_xx, z_xo, z_ox, z_oo)

def mat_a(a):
    return (inf, a, 0, a)

def e():
    #xoやoxの状態が変わる遷移は禁止、状態そのままはタダ
    return (0, inf, inf, 0)

def matvec(a,x):
    a_xx, a_xo, a_ox, a_oo = a
    x_x, x_o = x
    z_x = min(x_x + a_xx, x_o + a_ox)
    z_o = min(x_x + a_xo, x_o + a_oo)
    return (z_x, z_o)
```

## Bitwise matrix

```python
"""
bit演算を行列にのせる
https://atcoder.jp/contests/aalc001/submissions/80203522
演算*について、
0*x = y0, ~0*x = y1 と定める
M(x) = [~y0, ~y1
         y0,  y1]
v(x) = [~x,
         x]
とすると、
(OR,AND)半環で
M(y)v(x) = v(x*y)
OR: 単位元は0 -> 足し算
AND: 単位元は1 -> かけざん
"""
length = 30
inv0 = (1<<length)-1
# y0 = 0*x, y1=~0*x
# nand: y0 = inv0, y1 = inv0^x
def m(x):
    return (0, x, inv0, inv0^x)
e = (inv0, 0, 0, inv0)
def op(x,y):
    return (
        (y[0]&x[0])|(y[1]&x[2]),
        (y[0]&x[1])|(y[1]&x[3]),
        (y[2]&x[0])|(y[3]&x[2]),
        (y[2]&x[1])|(y[3]&x[3])
    )

def mul(m,x):
    return (m[2]&(inv0^x))|(m[3]&x)
```
