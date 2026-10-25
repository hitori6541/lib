# Source: https://github.com/hitori6541/lib
# File: geometry/vec.py

import math
class Vec:
    __slots__ = ("x", "y")
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return f"Vec{self.x, self.y}"
    def __add__(self, vv:"Vec"): return Vec(self.x+vv.x, self.y+vv.y)
    def __sub__(self, vv:"Vec"): return Vec(self.x-vv.x, self.y-vv.y)
    def __mul__(self, k:float): return Vec(self.x*k, self.y*k)
    __rmul__ = __mul__
    def dot(self, vv:"Vec"): return self.x*vv.x + self.y*vv.y
    def norm2(self): return self.x*self.x + self.y*self.y
    def norm(self):  return math.hypot(self.x, self.y)
    def cross(self, vv:"Vec"): return self.x*vv.y - self.y*vv.x
    def rot(self, a):
        nx = self.x*math.cos(a)-self.y*math.sin(a)
        ny = self.x*math.sin(a)+self.y*math.cos(a)
        return Vec(nx, ny)
    def cos(self, vv:"Vec"):
        return self.dot(vv)/self.norm()/vv.norm()

"""
射影 a を b方向に
c = a.dot(b) / b.norm2() * b 
向きがbと同じ aをb上に投射した

cross(i,j) = xi*yj - xj*yi
平行四辺形の符号付面積
反時計回りが正
"""
