# Source: https://github.com/hitori6541/lib
# File: data_structure/interval_set.py
# 使う: https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
# TODO: 軽量化

# region SortedSet
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, TypeVar
T = TypeVar('T')
class SortedSet(Generic[T]):
    BUCKET_RATIO = 16
    SPLIT_RATIO = 24
    
    def __init__(self, a: Iterable[T] = []) -> None:
        "Make a new SortedSet from iterable. / O(N) if sorted and unique / O(N log N)"
        a = list(a)
        n = len(a)
        if any(a[i] > a[i + 1] for i in range(n - 1)):
            a.sort()
        if any(a[i] >= a[i + 1] for i in range(n - 1)):
            a, b = [], a
            for x in b:
                if not a or a[-1] != x:
                    a.append(x)
        n = self.size = len(a)
        num_bucket = int(math.ceil(math.sqrt(n / self.BUCKET_RATIO)))
        self.a = [a[n * i // num_bucket : n * (i + 1) // num_bucket] for i in range(num_bucket)]

    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i: yield j

    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i): yield j
    
    def __eq__(self, other) -> bool:
        return list(self) == list(other)
    
    def __len__(self) -> int:
        return self.size
    
    def __repr__(self) -> str:
        return "SortedSet" + str(self.a)
    
    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"

    def _position(self, x: T) -> tuple[list[T], int, int]:
        "return the bucket, index of the bucket and position in which x should be. self must not be empty."
        for i, a in enumerate(self.a):
            if x <= a[-1]: break
        return (a, i, bisect_left(a, x))

    def __contains__(self, x: T) -> bool:
        if self.size == 0: return False
        a, _, i = self._position(x)
        return i != len(a) and a[i] == x

    def add(self, x: T) -> bool:
        "Add an element and return True if added. / O(√N)"
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        a, b, i = self._position(x)
        if i != len(a) and a[i] == x: return False
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.SPLIT_RATIO:
            mid = len(a) >> 1
            self.a[b:b+1] = [a[:mid], a[mid:]]
        return True
    
    def _pop(self, a: list[T], b: int, i: int) -> T:
        ans = a.pop(i)
        self.size -= 1
        if not a: del self.a[b]
        return ans

    def discard(self, x: T) -> bool:
        "Remove an element and return True if removed. / O(√N)"
        if self.size == 0: return False
        a, b, i = self._position(x)
        if i == len(a) or a[i] != x: return False
        self._pop(a, b, i)
        return True
    
    def lt(self, x: T) -> T | None:
        "Find the largest element < x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x: T) -> T | None:
        "Find the largest element <= x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x: T) -> T | None:
        "Find the smallest element > x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x: T) -> T | None:
        "Find the smallest element >= x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]
    
    def __getitem__(self, i: int) -> T:
        "Return the i-th element."
        if i < 0:
            for a in reversed(self.a):
                i += len(a)
                if i >= 0: return a[i]
        else:
            for a in self.a:
                if i < len(a): return a[i]
                i -= len(a)
        raise IndexError
    
    def pop(self, i: int = -1) -> T:
        "Pop and return the i-th element. / pop(0)->min / pop(-1)->max"
        if i < 0:
            for b, a in enumerate(reversed(self.a)):
                i += len(a)
                if i >= 0: return self._pop(a, ~b, i)
        else:
            for b, a in enumerate(self.a):
                if i < len(a): return self._pop(a, b, i)
                i -= len(a)
        raise IndexError
    
    def index(self, x: T) -> int:
        "Count the number of elements < x."
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        "Count the number of elements <= x."
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans

# endregion

# region IntervalSet
class IntervalSet():
    """
    manage intervals [l,r)
    count the number of elements
    need SortedSet by tatyam
    https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
    """
    data = None    
    def __init__(self, inf_ = 1<<60):
        self.inf = inf_
        self.banpei = {(-self.inf,-self.inf), (self.inf, self.inf)}
        self.data = SortedSet(self.banpei)
        self.cnt = 0

    def __iter__(self):
        for seg in self.data:
            if seg not in self.banpei:
                yield seg
    def __str__(self) -> str:
        return str(list(self))
    def __repr__(self) -> str:
        return str(self)
    
    def add_range(self, l0, r0):        
        """
        add [l0,r0)
        merge if intervals cross
        """
        assert (-self.inf < l0 < self.inf) and (-self.inf < r0 < self.inf)
        diff = r0 - l0
        if diff <= 0: return 0
        while True:
            lj, rj = self.data.ge((l0,-self.inf)) 
            if lj > r0: break
            self.data.discard((lj, rj))
            diff -= rj-lj
            diff += max(0,rj-r0); r0 = max(r0,rj)
        while True:
            li, ri = self.data.le((l0,self.inf))
            if ri < l0: break
            self.data.discard((li, ri))
            diff -= ri-li
            diff += l0-li; l0 = li
            diff += max(0,ri-r0); r0 = max(r0,ri)
        self.data.add((l0, r0))
        self.cnt += diff
        return diff
    def add_point(self, x):
        return self.add_range(x,x+1)
    def del_range(self, l0, r0):
        assert (-self.inf < l0 < self.inf) and (-self.inf < r0 < self.inf)
        if l0 >= r0: return 0
        diff = 0
        while True:
            lj, rj = self.data.ge((l0,-self.inf)) 
            if lj >= r0: break
            self.data.discard((lj, rj))
            diff -= rj-lj
            if rj <= r0: continue
            self.data.add((r0, rj))
            diff += rj-r0
        while True:
            li, ri = self.data.le((l0,self.inf)) 
            if ri <= l0: break
            self.data.discard((li, ri))
            diff -= ri-li
            if l0 <= li: continue
            self.data.add((li, l0)); diff += l0-li
            if r0 < ri: self.data.add((r0, ri)); diff += ri-r0
        self.cnt += diff
        return diff
    def del_point(self, x):
        return self.del_range(x,x+1)
    def cover(self, l0, r0):
        if r0 - l0 <= 0: return False
        _, ri = self.data.le((l0,self.inf)) 
        return l0 < r0 <= ri
    def cross(self, l0, r0):
        if r0 - l0 <= 0: return False
        _, ri = self.data.le((l0,self.inf))
        if l0 < ri: return True
        lj, _ = self.data.ge((l0,-self.inf))
        return lj < r0
    def contains(self, x):
        _, r = self.data.le((x, self.inf))
        return x < r
# endregion