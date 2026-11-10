# Source: https://github.com/hitori6541/lib
# File: optimization/monotone_cht.py
# submit: https://atcoder.jp/contests/dp/submissions/80750378

from collections import deque
class MonotoneCHT:
    """
    Convex Hull Trick for minimum queries.

    Requirements:
        - Added slopes are strictly decreasing.
        - Query x values are non-decreasing.

    Operations:
        push((a, b)): Add y = ax + b.
        query(x): Return the minimum value at x.

    Amortized O(1) per operation.
    O(N) total space.
    """
    def __init__(self, line: tuple[int, int]):
        """Initialize with one line (a, b) representing y = ax + b."""
        self.q = deque([line])

    def _f(self, line: tuple[int, int], x: int):
        return line[0] * x + line[1]

    def _bad(self, l1, l2, l3):
        # 傾き a1 > a2 > a3
        a1, b1 = l1
        a2, b2 = l2
        a3, b3 = l3
        # 交点の x 座標が x12 >= x23 なら l2 は不要
        return (b2 - b1) * (a2 - a3) >= (b3 - b2) * (a1 - a2)

    def query(self, x: int):
        q = self.q
        f = self._f
        while len(q) >= 2 and f(q[0], x) >= f(q[1], x):
            q.popleft()
        return self._f(q[0], x)

    def push(self, line: tuple[int, int]):
        q = self.q
        bad = self._bad
        assert q[-1][0] > line[0]
        while len(q) >= 2 and bad(q[-2], q[-1], line):
            q.pop()
        q.append(line)
