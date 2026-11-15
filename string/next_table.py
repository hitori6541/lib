# Source: https://github.com/hitori6541/lib
# File: string/next_table.py

from typing import Optional
class NextTable:
    """各仕切りからの右向きの遷移を全て持つ。

    nxt[i][j] は仕切り i から chars[j] を選んだ後の仕切り。
    次の出現がなければ None。index は要素から列番号を引く辞書。
    aa の要素はハッシュ可能で、sort=True のときは互いに比較可能とする。
    sort=True では列を昇順に並べる。sort=False では列順は未規定。

    計算量（N は列の長さ、σ は異なる要素数、M は検索パターンの長さ）
    - 構築は O(Nσ) 時間、O(Nσ) 空間。
    - next_pos は O(1) 時間、is_subsequence は O(M) 時間。
    """

    def __init__(self, aa, sort: bool = True) -> None:
        self.chars = list(set(aa))
        if sort:
            self.chars.sort()
        self.index = {c: j for j, c in enumerate(self.chars)}
        encoded = [self.index[c] for c in aa]

        row: list[Optional[int]] = [None] * len(self.chars)
        nxt = [row]
        for i in range(len(encoded) - 1, -1, -1):
            row = row.copy()
            row[encoded[i]] = i + 1
            nxt.append(row)
        nxt.reverse()
        self.nxt = nxt

    def next_pos(self, i: int, c) -> Optional[int]:
        """仕切り i から要素 c を選んだ行き先を返す。なければ None。"""
        j = self.index.get(c)
        if j is None:
            return None
        return self.nxt[i][j]

    def is_subsequence(self, pattern, start: int = 0) -> bool:
        """仕切り start 以降から pattern を部分列として選べるか返す。"""
        i = start
        for c in pattern:
            ni = self.next_pos(i, c)
            if ni is None:
                return False
            i = ni
        return True