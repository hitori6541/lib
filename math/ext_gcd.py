
import sys; sys.setrecursionlimit(10**6)
def ext_gcd(a,b):
    # 拡張ユークリッド
    # ax + by = gcd(a,b)
    # a>=0, b>=0, a=b=0は壊れる(gcd(0,0)は未定義)
    # (gcd,x,y)を返す
    if b == 0:
        return a, 1, 0
    else:
        res, s, t = ext_gcd(b, a%b)
        return res, t, s - a//b*t

import sys
sys.setrecursionlimit(10**6) 
def gojo(x, y):
    if y == 0:
        return x
    else:
        return gojo(y, x % y)

def gojo(a, b):
    while b != 0:
        a, b = b, a%b        
    return a