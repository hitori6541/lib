
"""
困ったときに見るやつ
https://kanpurin.hatenablog.com/entry/2021/09/15/220913
https://qiita.com/drken/items/f2ea4b58b0d21621bd51
https://w.atwiki.jp/uwicoder/pages/2118.html
"""

class Comb:
    """
    Precompute factorials / inv factorials up to max_n under mod (prime).
    - nCr, nPr, nHr (stars and bars)
    """
    __slots__ = ("max_n", "mod", "inv", "fact", "factinv")

    def __init__(self, max_n: int, mod: int):
        self.max_n = max_n
        self.mod = mod

        inv = [1] * (max_n + 1)
        fact = [1] * (max_n + 1)
        factinv = [1] * (max_n + 1)

        for i in range(2, max_n + 1):
            inv[i] = mod - inv[mod % i] * (mod // i) % mod

        for i in range(2, max_n + 1):
            fact[i] = fact[i - 1] * i % mod
            factinv[i] = factinv[i - 1] * inv[i] % mod

        self.inv = inv
        self.fact = fact
        self.factinv = factinv

    def _check_n(self, n: int):
        if n > self.max_n:
            raise ValueError(f"n={n} exceeds precomputed max_n={self.max_n}")

    def ncr(self, n: int, r: int) -> int:
        if n < 0 or r < 0 or n < r:
            return 0
        self._check_n(n)
        mod = self.mod
        return self.fact[n] * self.factinv[r] % mod * self.factinv[n - r] % mod

    def npr(self, n: int, r: int) -> int:
        if n < 0 or r < 0 or n < r:
            return 0
        self._check_n(n)
        mod = self.mod
        return self.fact[n] * self.factinv[n - r] % mod

    def nhr(self, n: int, r: int) -> int:
        """
        nHr = (n+r-1)C(r)  (n types, choose r with repetition)
        Conventions:
          - r < 0 -> 0
          - n == 0:
              r == 0 -> 1  (empty multiset)
              r > 0  -> 0
        """
        if r < 0:
            return 0
        if n == 0:
            return 1 if r == 0 else 0
        # need factorial up to n+r-1
        m = n + r - 1
        self._check_n(m)
        return self.ncr(m, r)

class CombTable:
    """
    O(nr) n*r<1e7, any mod
    """
    def __init__(self, n, mod = 998244353):
        self.n = n
        C = [[0]*(n+1) for _ in range(n+1)]
        for i in range(n+1):
            C[i][0] = 1
            for j in range(1,i+1):
                C[i][j] = (C[i-1][j-1] + C[i-1][j])%mod
        self.table = C
    def ncr(self, n, r):
        assert n <= self.n
        if n < 0 or r < 0 or n < r:
            return 0
        else:
            return self.table[n][r]
