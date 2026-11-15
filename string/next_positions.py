# Source: https://github.com/hitori6541/lib
# File: string/next_positions.py
# Submit: https://atcoder.jp/contests/tdpc/submissions/80870447

from bisect import bisect_right
from collections.abc import Iterator
from typing import Optional
class NextPositions:
    """文字列の仕切り i (0 <= i <= len(s)) を使って部分列の遷移を扱う。
    場所i から s[j] (i<=j) を選ぶと 場所j+1 に進む。
    pos[c][i] := i番目のcを選んだ時の遷移先

    計算量（N は文字列長、σ は文字種数、m は文字 c の出現回数）
    - 構築は O(N + σ log σ) 時間、O(N) 空間。
    - forward_updates / backward_updates は全件で O(N) 時間、O(σ) 補助空間。
    - next_pos は O(1 + log(m + 1)) 時間、O(1) 補助空間。
    - transitions は全件で O(σ log(N + 1)) 時間、O(1) 補助空間。
    """

    def __init__(self, s: str) -> None:
        self._s = s
        self.pos: dict[str, list[int]] = {}
        for i, c in enumerate(s, start=1):
            self.pos.setdefault(c, []).append(i)
        self._chars = sorted(self.pos)

    def forward_updates(self) -> Iterator[tuple[int, str, int, Optional[int]]]:
        """仕切りを i から i+1 に進めるときの差分を i=0 から順に返す。

        各差分は (i, s[i], 古い行き先=i+1, 新しい行き先)。
        s[i] の次の出現がなければ新しい行き先は None。
        """
        seen: dict[str, int] = {}
        for i, c in enumerate(self._s):
            j = seen.get(c, 0) + 1
            seen[c] = j
            positions = self.pos[c]
            new = positions[j] if j < len(positions) else None
            yield i, c, i + 1, new

    def backward_updates(self) -> Iterator[tuple[int, str, Optional[int], int]]:
        """仕切りを i+1 から i に戻すときの差分を i=len(s)-1 から順に返す。

        各差分は (i, s[i], 古い行き先, 新しい行き先=i+1)。
        s[i+1:] に s[i] がなければ古い行き先は None。
        """
        nxt: dict[str, int] = {}
        for i in range(len(self._s) - 1, -1, -1):
            c = self._s[i]
            old = nxt.get(c)
            new = i + 1
            nxt[c] = new
            yield i, c, old, new

    def next_pos(self, i: int, c: str) -> Optional[int]:
        """仕切り i から文字 c を選んだ行き先を返す。なければ None。"""
        positions = self.pos.get(c)
        if positions is None:
            return None
        j = bisect_right(positions, i)
        if j < len(positions):
            return positions[j]
        return None

    def transitions(self, i: int) -> Iterator[tuple[str, int]]:
        """仕切り i から選べる (文字, 行き先) を文字の昇順で返す。"""
        for c in self._chars:
            ni = self.next_pos(i, c)
            if ni is not None:
                yield c, ni
