
from collections import Counter
class Eratos:
    # need "Counter"
    __slots__ = ("lim", "spf", "isprime", "primes")
    def __init__(self, lim: int):
        assert lim > 0
        # O(lim * log(log(lim)))
        self.lim = lim
        spf = list(range(lim + 1))
        if lim >= 1:
            spf[0] = 0
            spf[1] = 1
        r = int(lim ** 0.5)
        for p in range(2, r + 1):
            if spf[p] == p:
                start = p * p
                step = p
                for j in range(start, lim + 1, step):
                    if spf[j] == j:
                        spf[j] = p
        self.spf = spf
        isprime = [False]*(lim+1)
        primes = []
        for i in range(2,lim+1):
            if spf[i] == i:
                isprime[i] = True
                primes.append(i)
        self.isprime = isprime
        self.primes = primes
    
    def factorize_small(self, x: int):
        # O(log x)
        assert 1 <= x <= self.lim
        ret = Counter()
        while x > 1:
            p = self.spf[x]
            while x % p == 0:
                x //= p
                ret[p] += 1
        return ret
    
    def factorize_large(self, x: int):
        # O(√x / log x)
        assert 1 <= x <= self.lim**2,f"x={x}"
        ret = Counter()
        for p in self.primes:
            if p*p > x:
                break
            while x%p == 0:
                x //= p
                ret[p] += 1
            if x <= self.lim:
                ret.update(self.factorize_small(x))
                return ret
        if x > 1:
            ret[x] += 1
        return ret

    def factorize(self, x: int) -> Counter:
        assert 1 <= x <= self.lim**2
        if x <= self.lim:
            return self.factorize_small(x)
        else:
            return self.factorize_large(x)
    
    def divisors(self, x: int, *, sort: bool = True):
        """Return list of all positive divisors of x."""
        assert 1 <= x <= self.lim**2
        fs = self.factorize(x)          # Counter {p: e}
        divs = [1]
        for p, e in fs.items():
            base = 1
            add = []
            for _ in range(e):
                base *= p
                # 既存のdivsそれぞれに p^k を掛ける
                for d in divs:
                    add.append(d * base)
            divs += add
        if sort:
            divs.sort()
        return divs

    def mebius(self,x):
        ret = 1
        while x > 1:
            p = self.spf[x]
            if x%(p*p) == 0:
                return 0
            x //= p
            ret *= -1
        return ret

