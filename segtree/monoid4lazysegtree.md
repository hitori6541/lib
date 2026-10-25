# LazySegtree モノイド集

> **Source:** https://github.com/hitori6541/lib  
> **File:** `segtree/monoid4lazysegtree.md`

## 目次

- [LazySegtree モノイド集](#lazysegtree-モノイド集)
  - [目次](#目次)
  - [General](#general)
  - [RangeAdd\_RangeMin](#rangeadd_rangemin)
  - [RangeAdd\_RangeSum (packedint)](#rangeadd_rangesum-packedint)
  - [RangeAdd\_RangeSum (tuple)](#rangeadd_rangesum-tuple)
  - [RangeLet\_RangeMin](#rangelet_rangemin)
  - [RangeLet\_RangeSum (tuple)](#rangelet_rangesum-tuple)
  - [RangeAdd\_RangeSquareSum (cnt, sum, squaresum)](#rangeadd_rangesquaresum-cnt-sum-squaresum)
  - [RangeAffine\_RangeSum (tuple)](#rangeaffine_rangesum-tuple)

## General

```python
e = 0
ide = 0
def op(x, y):
    return 
def mapp(f, x):
    return 
def comp(f, g): #g. then f.
    return 
lz = LazySegtree([e for _ in range(n)],op,e,mapp,comp,ide)
```

## RangeAdd_RangeMin

```python
e = inf
ide = 0
def op(x, y):
    return min(x,y)
def mapp(f, x):
    return f + x
def comp(f, g): #g. then f.
    return f + g
lz = LazySegtree([e for _ in range(n)],op,e,mapp,comp,ide)
```

## RangeAdd_RangeSum (packedint)

```python
"""
# 2整数を1整数にpack
k = 32
mask = (1<<k) - 1

# pack: (x,y) -> v
v = (x<<k) | y

# unpack: v -> (x,y)
x, y = v>>k, v&mask
"""
# (sum,len) -> sum<<k + len
k = 21
mask = (1<<k) - 1
list_ = [1] * n
e = 0
ide = 0
def op(x, y):
    return x + y
def mapp(f, x):
    return x + ((f*(x&mask))<<k)
def comp(f, g):
    return f + g
g = LazySegtree(list_,op,e,mapp,comp,ide)
```

## RangeAdd_RangeSum (tuple)

```python
list_ = [(0,1)] * n
e = (0, 0)
ide = 0
def op(x, y):
    return (x[0] + y[0], x[1] + y[1])
def mapp(f, x):
    return (x[0] + f * x[1], x[1])
def comp(f, g):
    return f + g
g = LazySegtree(list_,op,e,mapp,comp,ide)
```

## RangeLet_RangeMin

```python
e = inf
ide = -1
def op(x, y):
    return min(x,y)
def mapp(f, x):
    return f if f != ide else x
def comp(f, g): #g. then f.
    return f if f != ide else g
lz = LazySegtree([e for _ in range(n)],op,e,mapp,comp,ide)
```

## RangeLet_RangeSum (tuple)

```python
list_ = [(0, 1)] * n
e = (0, 0)
ide = inf
def op(x, y):
    return (x[0] + y[0], x[1] + y[1])
def mapp(f, x):
    return (f * x[1], x[1]) if f != ide else (x[0], x[1])
def comp(f, g): #g. then f.
    return f if f != ide else g
lz = LazySegtree(list_,op,e,mapp,comp,ide)
```

## RangeAdd_RangeSquareSum (cnt, sum, squaresum)

```python
list_ = [(1,0,0)] * n
e = (0, 0, 0)
ide = 0
def op(x, y):
    return (x[0]+y[0], x[1]+y[1], x[2]+y[2])
def mapp(f, x):
    return (x[0], x[1]+f*x[0], x[2]+2*f*x[1]+x[0]*f*f)
def comp(f, g): #g. then f.
    return f + g
lz = LazySegtree(list_,op,e,mapp,comp,ide)
```

## RangeAffine_RangeSum (tuple)

```python
list_ = [(0,1)]*n
mod = 998244353
e = (0, 0)
ide = (1, 0)
def op(x, y):
    return (
        (x[0]+y[0])%mod,
        (x[1]+y[1])
    )
def mapp(f, x):
    # f = (b,c)
    # x <- b*x + c
    return (
        (f[0]*x[0] + f[1]*x[1])%mod, 
        x[1]
    )
def comp(f, g):
    return (
        f[0]*g[0]%mod, 
        (g[1]*f[0] + f[1])%mod
    )
lz = LazySegtree(list_,op,e,mapp,comp,ide)
```
