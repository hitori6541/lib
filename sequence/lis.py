
import bisect
def lis(seq):
    if len(seq) == 0:
        return 0
    LIS = [seq[0]]
    for i in range(len(seq)):
        if seq[i] > LIS[-1]:
            LIS.append(seq[i])
        else:
            LIS[bisect.bisect_left(LIS, seq[i])] = seq[i]
    return len(LIS)