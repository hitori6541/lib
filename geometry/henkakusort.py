# https://blog.ngtkana.com/entry/2021/11/13/202103
# functoolsは遅いので、自前ソートを使うと吉 -> sequence/merge_sort.py

def cmp_arg_zero(p: tuple[int, int], q: tuple[int, int]):
    # 0 <= theta < 2pi
    # pが小さい：-1

    # [0,pi), [pi,2*pi)の比較
    px, py = p
    qx, qy = q
    ap = py > 0 or (py == 0 and px > 0)
    aq = qy > 0 or (qy == 0 and qx > 0)
    if ap != aq:
        return -1 if ap else 1

    # 外積
    z = px * qy - py * qx
    return (z < 0) - (z > 0)
    
def cmp_arg_negpi(p: tuple[int, int], q: tuple[int, int]):
    # https://judge.yosupo.jp/submission/349420
    # -pi < theta <= pi
    # pが小さい：-1

    # (-pi,0], (0,pi]の比較
    px, py = p
    if px == 0 and py == 0:
        px = 1
    qx, qy = q
    if qx == 0 and qy == 0:
        qx = 1
    ap = py < 0 or (py == 0 and px >= 0)
    aq = qy < 0 or (qy == 0 and qx >= 0)
    if ap != aq:
        return -1 if ap else 1

    #外積
    z = px * qy - py * qx
    return (z < 0) - (z > 0)

"""
# 一応使用例
from functools import cmp_to_key
n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]

# 点のソート
points.sort(key=cmp_to_key(cmp_arg))

# 添え字のソート
order = sorted(
    range(n),
    key=cmp_to_key(lambda i, j: cmp_arg(points[i], points[j]))
)
"""