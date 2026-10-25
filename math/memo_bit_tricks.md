# ビット操作メモ

> **Source:** https://github.com/hitori6541/lib  
> **File:** `math/memo_bit_tricks.md`

```python
#  rem の全部分集合 sub を列挙（sub は rem の部分集合）
sub = rem
while True:
    # sub を使った処理
    # ...

    if sub == 0:
        break
    sub = (sub - 1) & rem
```

```python
# 空集合なし版
sub = rem
while sub:
    # sub を使った処理
    # ...

    sub = (sub - 1) & rem
```

```python
# LSB / MSB
# x > 0
#LSB = Least Significant Bit 最下位ビット
lsb = (x&-x).bit_length()-1
#MSB = Most Significant Bit 最上位ビット
msb = x.bit_length()-1
```
