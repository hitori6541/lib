
class PrefixSumND:
    def __init__(self, length: list[int]):
        """N次元累積和 (l+1)の総積ぶんメモリつかう
        ABC465-F Sjeltzer?
        https://atcoder.jp/contests/abc465/submissions/77234011
        """
        assert len(length) > 0
        assert all(l > 0 for l in length)
        self.dim = len(length)
        self.length = length[:]
        # [l, r) クエリを楽にするため、内部は各次元 +1
        self.shape = [l + 1 for l in length]
        N = 1
        stride = []
        for l in self.shape:
            stride.append(N)
            N *= l
        self.N = N
        self.stride = stride
        self.data = [0] * N
        self.built = False

    def _idx(self, pos: list[int]) -> int:
        assert len(pos) == self.dim
        idx = 0
        for x, p in zip(pos, self.stride):
            idx += x * p
        return idx

    def set(self, pos: list[int], val: int):
        assert not self.built
        assert len(pos) == self.dim
        for x, l in zip(pos, self.length):
            assert 0 <= x < l, f"pos:{pos}"
        # 元座標 pos は内部では pos+1 に置く
        inner = [x + 1 for x in pos]
        self.data[self._idx(inner)] = val

    def add(self, pos: list[int], val: int):
        assert not self.built
        assert len(pos) == self.dim
        for x, l in zip(pos, self.length):
            assert 0 <= x < l, f"pos:{pos}"
        inner = [x + 1 for x in pos]
        self.data[self._idx(inner)] += val

    def build(self):
        assert not self.built
        data = self.data
        shape = self.shape
        stride = self.stride
        N = self.N
        # 各次元方向に1次元累積和を流す
        for d in range(self.dim):
            p = stride[d]
            size = shape[d]
            block = p * size
            for base in range(0, N, block):
                for offset in range(p):
                    for k in range(1, size):
                        cur = base + k * p + offset
                        data[cur] += data[cur - p]
        self.built = True

    def sum(self, left: list[int], right: list[int]) -> int:
        """
        sum of left[i] <= x[i] < right[i] for all i
        [l0,r0)かつ[l1,r1)かつ...[ln,rn)
        l > r は外で処理しとく
        O(d*2^d)
        """
        assert self.built
        assert len(left) == self.dim, f"left:{left}, right:{right}"
        assert len(right) == self.dim, f"left:{left}, right:{right}"
        for l, r, length in zip(left, right, self.length):
            assert 0 <= l <= r <= length, f"left:{left}, right:{right}"
        res = 0
        for bit in range(1 << self.dim):
            idx = 0
            sign = 1
            for d in range(self.dim):
                if (bit >> d) & 1:
                    idx += left[d] * self.stride[d]
                    sign *= -1
                else:
                    idx += right[d] * self.stride[d]
            res += sign * self.data[idx]
        return res