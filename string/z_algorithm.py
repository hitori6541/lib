
# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/acl_string.py
# z配列 [s[i:] と s の最大共通接頭辞のサイズ for i in range(len(s))]
# s = "abcaabc" -> z = [7,0,0,1,3,2,1]
def z_algorithm(s):
    n = len(s)
    if n == 0: return []
    z = [0] * n; i = 1; j = 0
    while i < n:
        z[i] = 0 if (j + z[j] <= i) else min(j + z[j] - i, z[i - j])
        while (i + z[i] < n) and (s[z[i]] == s[i + z[i]]): z[i] += 1
        if j + z[j] < i + z[i]: j = i
        i += 1
    z[0] = n
    return z


