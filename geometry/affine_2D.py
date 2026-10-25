# Source: https://github.com/hitori6541/lib
# File: geometry/affine_2D.py

class affine2D:
    def __init__(self):
        # x -> a*x + b*y + c,  y -> d*x + e*y + f
        self.a, self.b, self.c = 1, 0, 0
        self.d, self.e, self.f = 0, 1, 0

    def affine(self, na, nb, nc, nd, ne, nf):
        """
        新しい変換 S:
          x -> na*x + nb*y + nc
          y -> nd*x + ne*y + nf
        を「後から」合成する:  self := S ∘ self
        """
        a, b, c = self.a, self.b, self.c
        d, e, f = self.d, self.e, self.f
        self.a = na*a + nb*d
        self.b = na*b + nb*e
        self.c = na*c + nb*f + nc
        self.d = nd*a + ne*d
        self.e = nd*b + ne*e
        self.f = nd*c + ne*f + nf

    def rot90(self, t: int):
        t %= 4
        if t == 0:
            return
        elif t == 1:   # CCW: (x,y)->(-y,x)
            self.affine(0, -1, 0,  1, 0, 0)
        elif t == 2:   # 180: (x,y)->(-x,-y)
            self.affine(-1, 0, 0,  0, -1, 0)
        else:          # CW: (x,y)->(y,-x)
            self.affine(0, 1, 0,  -1, 0, 0)

    def mul(self, sx, sy):
        # (x,y)->(sx*x, sy*y)
        self.affine(sx, 0, 0,  0, sy, 0)

    def slide(self, tx, ty):
        # (x,y)->(x+tx, y+ty)
        self.affine(1, 0, tx,  0, 1, ty)

    def mapping(self, x, y):
        return (self.a*x + self.b*y + self.c,
                self.d*x + self.e*y + self.f)