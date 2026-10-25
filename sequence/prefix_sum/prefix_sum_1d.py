
class PrefixSum1D:
    def __init__(self,list_:list):
        self.n = len(list_)
        data = [0] + list_
        for i in range(self.n):
            data[i+1] += data[i]        
        self.data = data
    def sum(self, l:int,r:int):
        #sum of [l,r)
        assert 0 <= l <= r <= self.n
        return self.data[r] - self.data[l]

