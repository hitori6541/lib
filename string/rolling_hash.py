# Source: https://github.com/hitori6541/lib
# File: string/rolling_hash.py

import random
from collections import deque
class RollingHash():
    """
    def f(c): return ord(c) - ord("a")
    """
    p1 = 998244353; p2 = 10**9+7
    b1 = random.randrange(2, p1); b2 = random.randrange(2, p2)
    # b1 = 10; b2 = 100
    inv1 = pow(b1, -1, p1); inv2 = pow(b2, -1, p2)
    def __init__(self, string = None):        
        self.v1 = 0
        self.v2 = 0
        self.w1 = 1
        self.w2 = 1
        self.q = deque()
        self.l = 0
        if string is not None:
            for c in string:
                self.append(c)

    def __eq__(self, other):
        if not isinstance(other, RollingHash): return NotImplemented
        #assert (self.b1, self.p1, self.b2, self.p2) == (other.b1, other.p1, other.b2, other.p2)
        return self.l == other.l and self.v1 == other.v1 and self.v2 == other.v2

    def append(self, c):
        self.q.append(c)
        self.v1 = ((self.v1 * self.b1) + c) % self.p1
        self.v2 = ((self.v2 * self.b2) + c) % self.p2
        self.l += 1
        self.w1 = (self.w1 * self.b1) % self.p1
        self.w2 = (self.w2 * self.b2) % self.p2
    
    def appendleft(self, c):
        self.q.appendleft(c)
        self.v1 = (self.v1 + c * self.w1) % self.p1
        self.v2 = (self.v2 + c * self.w2) % self.p2
        self.l += 1
        self.w1 = (self.w1 * self.b1) % self.p1
        self.w2 = (self.w2 * self.b2) % self.p2
    
    def pop(self):
        assert self.l > 0
        c = self.q.pop()
        self.v1 = (self.v1 - c) * self.inv1 % self.p1
        self.v2 = (self.v2 - c) * self.inv2 % self.p2
        self.l -= 1
        self.w1 = (self.w1 * self.inv1) % self.p1
        self.w2 = (self.w2 * self.inv2) % self.p2
        return c
    
    def popleft(self):
        assert self.l > 0
        c = self.q.popleft()
        self.l -= 1
        self.w1 = (self.w1 * self.inv1) % self.p1
        self.w2 = (self.w2 * self.inv2) % self.p2
        self.v1 = (self.v1 - c * self.w1) % self.p1
        self.v2 = (self.v2 - c * self.w2) % self.p2
        return c

    def key(self):
        #setにぶち込む用
        return (self.l, self.v1, self.v2)