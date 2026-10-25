# Source: https://github.com/hitori6541/lib
# File: sequence/prefix_sum/prefix_sum_1d_mod.py

class PrefixSum1DMod:
    def __init__(self,list_:list,mod=998244353):
        self.n = len(list_)
        self.mod = mod
        data = [0] + [a%mod for a in list_]
        for i in range(self.n):
            data[i+1] += data[i]
            data[i+1] %= mod
        self.data = data
    def sum(self, l:int,r:int):
        #sum of [l,r)
        assert 0 <= l <= r <= self.n
        return (self.data[r] - self.data[l])%self.mod

