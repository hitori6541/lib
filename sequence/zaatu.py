# Source: https://github.com/hitori6541/lib
# File: sequence/zaatu.py

class Zaatu:
    def __init__(self, REV = False, OFFSET = 0):
        self.rev = REV
        self.offset = OFFSET
        self.vals = set()
        self.v = [] # i2val
        self.r = {} # val2i
        self.size = 0
        self.built = False
    def add(self, VALUES):
        assert not self.built
        if isinstance(VALUES, int):
            self.vals.add(VALUES)
        else:
            self.vals.update(VALUES)
    def build(self):
        assert not self.built
        self.v = sorted(self.vals, reverse = self.rev) 
        self.r = {x:i+self.offset for i,x in enumerate(self.v)}
        self.size = len(self.v)
        self.built = True
    def comp(self, LIST_):
        assert self.built
        return [self.r[v] for v in LIST_]


