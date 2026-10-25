# Source: https://github.com/hitori6541/lib
# File: data_structure/bit_set.py
# submit: https://atcoder.jp/contests/abc147/submissions/73870031

class BitSet:    
    def __init__(self, offset: int):
        #offset := abs(絶対値が一番大きい負の値)
        self.offset = offset
        self.bits = 0
    def add(self, v: int) -> None:
        self.bits |= 1 << (self.offset + v)
    def shift(self, d:int) -> None: #破壊的変更です
        if d >= 0: self.bits <<= d
        else: self.bits >>= (-d)
    def merge(self, other: "BitSet", d: int) -> None:
        #otherをdだけshiftしたものをマージする
        if d >= 0: self.bits |= other.bits << d
        else: self.bits |= other.bits >> (-d)
    def contains(self, v: int) -> bool:
        return (self.bits >> (self.offset + v)) & 1 == 1
    def values(self) -> list[int]:
        res = []; b = self.bits
        while b:
            lsb = b & -b
            idx = lsb.bit_length() - 1
            res.append(idx - self.offset)
            b ^= lsb
        return res
    def __contains__(self, v: int) -> bool:
        return self.contains(v)