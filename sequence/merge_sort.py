# Source: https://github.com/hitori6541/lib
# File: sequence/merge_sort.py

def merge_sorted(a:list, cmp:callable, reverse=False):
    """
    cmp(p,q) -> (p>q) - (p<q) 
    a: aの要素はイミュータブルが安全
    """
    n = len(a); w = 1
    src = a[:]; dst = [None] * n
    while w < n:
        for l in range(0, n, 2 * w):
            # [l,m)と[m,r)をマージする
            m = min(l + w, n); r = min(l + 2 * w, n)
            i, j, k = l, m, l
            while i < m and j < r:
                c = cmp(src[i], src[j])
                if (c <= 0) if not reverse else (c >= 0):
                    dst[k] = src[i]
                    i += 1
                else:
                    dst[k] = src[j]
                    j += 1
                k += 1
            while i < m:
                dst[k] = src[i]
                i += 1; k += 1
            while j < r:
                dst[k] = src[j]
                j += 1; k += 1
        src, dst = dst, src
        w *= 2
    return src