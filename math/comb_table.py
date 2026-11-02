# Source: https://github.com/hitori6541/lib
# File: math/comb_table.py

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
