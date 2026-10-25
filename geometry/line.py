# https://atcoder.jp/contests/abc467/tasks/abc467_d

from math import gcd
class Line2D:    
    def __init__(self, x1, y1, x2, y2):
        assert (x1, y1) != (x2, y2)
        a = y1 - y2
        b = x2 - x1
        c = x1 * y2 - x2 * y1

        # ax + by + c = 0 を正規化
        g = gcd(gcd(abs(a), abs(b)), abs(c))
        a //= g
        b //= g
        c //= g

        # a > 0、または a == 0 なら b > 0 に統一
        if a < 0 or (a == 0 and b < 0):
            a = -a
            b = -b
            c = -c

        self.a = a
        self.b = b
        self.c = c

    def is_parallel(self, other):
        return self.a * other.b == self.b * other.a

    def is_perpendicular(self, other):
        return self.a * other.a + self.b * other.b == 0

    def on_point(self, x, y):
        return self.a * x + self.b * y + self.c == 0

    def parallel_through(self, x, y):
        """
        自分と平行で、点 (x, y) を通る直線を返す。
        自分自身と一致する可能性もある。
        """
        # 自分の方向ベクトルは (b, -a)
        return Line2D(x, y, x+self.b, y-self.a)

    def perpendicular_through(self, x, y):
        """
        自分と垂直で、点 (x, y) を通る直線を返す。
        """
        # 垂直な直線の方向ベクトルは (a, b)
        return Line2D(x, y, x+self.a, y+self.b)

    def is_same(self, other):
        return (
            self.a == other.a
            and self.b == other.b
            and self.c == other.c
        )
    
    def has_common_point(self, other):
        return self.is_same(other) or not self.is_parallel(other)

    def __repr__(self):
        return f"Line_2D({self.a}x + {self.b}y + {self.c} = 0)"