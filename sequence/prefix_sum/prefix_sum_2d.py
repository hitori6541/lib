
class PrefixSum2D:
    def __init__(self, h:int, w:int):
        assert h > 0 and w > 0        
        self.h = h
        self.w = w
        self.data = [[0]*(w+1) for _ in range(h+1)]
        self.built = False

    def set(self, y:int, x:int, val:int):
        assert not self.built
        assert 0 <= y < self.h and 0 <= x < self.w, f"y:{y}, x:{x}"
        self.data[y+1][x+1] = val
    def add(self, y:int, x:int, val:int):
        assert not self.built
        assert 0 <= y < self.h and 0 <= x < self.w, f"y:{y}, x:{x}"
        self.data[y+1][x+1] += val
    def copy(self, list_:list[list[int]]):
        assert not self.built
        assert len(list_) == self.h and all(len(list_[y]) == self.w for y in range(self.h))
        data = self.data
        for y in range(1,self.h+1):
            for x in range(1,self.w+1):
                data[y][x] = list_[y-1][x-1]

    def build(self):
        assert not self.built        
        data = self.data
        for y in range(1, self.h + 1):
            for x in range(1, self.w + 1):
                data[y][x] += data[y][x-1] + data[y-1][x] - data[y-1][x-1]
        self.built = True

    def sum(self, y0:int, x0:int, y1:int, x1:int):
        assert self.built
        assert 0 <= y0 <= y1 <= self.h, f"y0:{y0}, y1:{y1}"
        assert 0 <= x0 <= x1 <= self.w, f"x0:{x0}, x1:{x1}"
        #sum of y0 <= y < y1 and x0 <= x < x1
        s = self.data
        return s[y1][x1] - s[y0][x1] - s[y1][x0] + s[y0][x0]

