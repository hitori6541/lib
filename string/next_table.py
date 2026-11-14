 # 作成中

def gen_next_table(aa:list, sort=True, inf=10**9):
    # O(σN)
    ss = list(set(aa))
    if sort:
        ss.sort()
    d = {s:i for i,s in enumerate(ss)}

    aa = [d[s] for s in aa]
    n = len(aa)
    m = len(ss)

    nxt = [[inf]*m for _ in range(n+1)]
    for i in range(n-1,-1,-1):
        for j in range(m):
            nxt[i][j] = nxt[i+1][j]
        nxt[i][aa[i]] = i+1
    return nxt

