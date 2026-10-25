# 幾何メモ

> **Source:** https://github.com/hitori6541/lib  
> **File:** `geometry/memo_geo.md`

```python
#誤差評価
import math
REL = 1e-12
ABS = 1e-12
def tol(a: float, b: float, rel: float = REL, abs_: float = ABS) -> float:
    # ゼロ近傍は abs_、それ以外は相対誤差でスケール追従
    return max(abs_, rel * max(abs(a), abs(b)))
def eq(a: float, b: float) -> bool:      # 1) a == b
    return abs(a - b) <= tol(a, b)
def gt(a: float, b: float) -> bool:      # 2) a > b
    # 「十分に大きい」ときだけ True（境界は False）
    return a - b > tol(a, b)
def ge(a: float, b: float) -> bool:      # 3) a >= b
    # b より小さくない（境界含む）
    return a - b >= -tol(a, b)
```
