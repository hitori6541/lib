# Source: https://github.com/hitori6541/lib
# File: optimization/li_chao_tree.py
# Submit: https://judge.yosupo.jp/submission/416267
# Submit: https://judge.yosupo.jp/submission/416271

from bisect import bisect_left, bisect_right
from typing import Iterable, Optional
class LiChaoTreeMin:
    """Coordinate-compressed Li Chao Tree for minimum queries.

    Initialization
        - LiChaoTreeMin(xs) registers a nonempty iterable of integer coordinates.
        - Duplicate coordinates are merged. The tree starts with no lines.

    Operations
        - add_line((a, b)) adds y = ax + b at all registered coordinates.
        - add_segment(l, r, (a, b)) adds it at registered x in [l, r].
        - get(x) returns the minimum at x, or None if no line covers it.
        - Slopes and query points may arrive in any order.
        - An unregistered query point or l > r raises ValueError.

    Complexity
        - M input coordinates, K distinct coordinates, H = 1 + log K.
        - Initialization takes expected O(M + K log K) time and O(K) space.
        - add_line takes O(H) time. add_segment takes O(H^2) time.
        - get takes expected O(H) time, including a dictionary lookup.
    """

    def __init__(self, xs: Iterable[int]) -> None:
        """WARNING — xs must be nonempty."""
        self._xs = sorted(set(xs))
        if not self._xs:
            raise ValueError("at least one coordinate is required")
        self._index = {x: i for i, x in enumerate(self._xs)}
        self._lines: list[Optional[tuple[int, int]]] = [None] * (4 * len(self._xs))

    @staticmethod
    def _f(line: tuple[int, int], x: int) -> int:
        return line[0] * x + line[1]

    def add_line(self, line: tuple[int, int]) -> None:
        self._push(line, 1, 0, len(self._xs) - 1)

    def add_segment(self, l: int, r: int, line: tuple[int, int]) -> None:
        if l > r:
            raise ValueError("segment must satisfy l <= r")
        xs = self._xs
        first = bisect_left(xs, l)
        last = bisect_right(xs, r) - 1
        if first > last:
            return

        stack = [(1, 0, len(xs) - 1)]
        while stack:
            node, left, right = stack.pop()
            if first <= left and right <= last:
                self._push(line, node, left, right)
                continue

            mid = (left + right) // 2
            if first <= mid:
                stack.append((2 * node, left, mid))
            if mid < last:
                stack.append((2 * node + 1, mid + 1, right))

    def _push(self, line: tuple[int, int], node: int, left: int, right: int) -> None:
        xs = self._xs
        lines = self._lines
        f = self._f

        while (current := lines[node]) is not None:
            mid = (left + right) // 2
            # 中点で小さい方をこのノードに残す。
            if f(line, xs[mid]) < f(current, xs[mid]):
                line, current = current, line
                lines[node] = current

            # 残りの直線が勝てる側だけに降りる。
            if f(line, xs[left]) < f(current, xs[left]):
                node *= 2
                right = mid
            elif f(line, xs[right]) < f(current, xs[right]):
                node = 2 * node + 1
                left = mid + 1
            else:
                return

        lines[node] = line

    def get(self, x: int) -> Optional[int]:
        idx = self._index.get(x)
        if idx is None:
            raise ValueError("x is not a registered coordinate")

        left, right = 0, len(self._xs) - 1
        node = 1
        lines = self._lines
        f = self._f
        best = None

        while True:
            line = lines[node]
            if line is not None:
                value = f(line, x)
                if best is None or value < best:
                    best = value
            # 空のノードにも、直線を持つ子孫があり得る。
            if left == right:
                return best

            mid = (left + right) // 2
            if idx <= mid:
                node *= 2
                right = mid
            else:
                node = 2 * node + 1
                left = mid + 1