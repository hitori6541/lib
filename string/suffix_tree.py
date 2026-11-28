# Source: https://github.com/hitori6541/lib
# File: string/suffix_tree.py
# shakayami: https://github.com/shakayami/ACL-for-python/blob/master/acl_string.py
# Original license: The Unlicense - https://github.com/shakayami/ACL-for-python/blob/master/LICENSE
# Submit: https://atcoder.jp/contests/past23-open/submissions/81114033

class SuffixTree:
    """ASCII の str から番兵なしの Suffix Tree を構築する。空文字列も可。

    s: 元の文字列。
    sa[i]: 辞書順で i 番目の非空 suffix の開始位置。
    lcp[i]: s[sa[i]:] と s[sa[i + 1]:] の最長共通接頭辞長。

    根はノード 0。par[0] = -1、depth[0] = pos[0] = length[0] = tail[0] = 0。
    par[v]: 親ノード番号。分岐を挿入するため par[v] < v とは限らない。
    pos[v]: ノードの文字列が s 上に現れる開始位置。
    depth[v]: 根からノード v までの文字列長。
    length[v]: 親から v までの辺の文字列長（depth[v] - depth[par[v]]）。
    tail[v]: suffix の終端なら 1、その他は 0。内部ノードも終端になりうる。
    child[v]: 辺の先頭文字の昇順に並ぶ子ノード。
    order: 根を含む辞書順の preorder。逆順にたどると子から親へ集約できる。

    ノードの文字列は s[pos[v]:pos[v] + depth[v]]。
    v != 0 への辺の文字列は s[pos[v] + depth[par[v]]:pos[v] + depth[v]]。
    例えば s = "banana" の "ana" は pos = 3, depth = 3。
    親 "a" の depth は 1 なので、辺の文字列は s[4:6] = "na" で length = 2。

    SA 順に追加し、直前の suffix への経路をスタックに持つ。
    LCP の深さまで戻り、LCP が辺の途中ならそこに分岐を挿入する。
    ノードは高々一度ずつ push/pop され、兄弟の順序は追加順から復元できる。
    SA・LCP の構築を含め、時間・空間ともに O(N)。木の構築・走査は反復処理。
    節点番号が対応するように、各配列は読み取り専用として扱う。
    """

    def __init__(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError("s must be an ASCII str")
        self.s = s
        n = len(s)
        sa = self.sa = self._sa_is(list(s.encode("ascii")), 127)
        lcp = self.lcp = self._lcp_array(s, sa)

        par = [-1]
        depth = [0]
        pos = [0]
        tail = bytearray(1)
        stack = [0]
        for i, start in enumerate(sa):
            shared_depth = lcp[i - 1] if i else 0
            last = -1
            while depth[stack[-1]] > shared_depth:
                last = stack.pop()
            p = stack[-1]
            if depth[p] < shared_depth:
                # 最後に pop した子とその親の間に分岐を作る。
                branch = len(par)
                par.append(p)
                depth.append(shared_depth)
                pos.append(pos[last])
                tail.append(0)
                par[last] = branch
                stack.append(branch)
                p = branch

            # 直前の suffix が現在の suffix の接頭辞なら、終端の下に追加する。
            stack.append(len(par))
            par.append(p)
            depth.append(n - start)
            pos.append(start)
            tail.append(1)
        stack.clear()

        m = len(par)
        length = [0] * m
        child = [[] for _ in range(m)]
        # SA 順では、新しい子は末尾に追加される。分岐の挿入でも末尾の
        # 子が新しい番号に置き換わるため、兄弟はノード番号順で復元できる。
        for v in range(1, m):
            p = par[v]
            length[v] = depth[v] - depth[p]
            child[p].append(v)

        order = []
        stack.append(0)
        while stack:
            v = stack.pop()
            order.append(v)
            stack.extend(reversed(child[v]))

        self.par = par
        self.depth = depth
        self.pos = pos
        self.tail = tail
        self.length = length
        self.child = child
        self.order = order

    def suffix_counts(self) -> list[int]:
        """各部分木の suffix 終端数を O(N) 時間・空間で返す。

        v != 0 ではノードの文字列の出現回数、根では len(s)。
        """
        cnt = list(self.tail)
        par = self.par
        for v in reversed(self.order):
            if v == 0:
                break
            cnt[par[v]] += cnt[v]
        return cnt

    def print_tree(self) -> None:
        """デバッグ用に辺の文字列とノード番号を標準エラーに表示する。* は suffix の終端。"""
        import sys

        stack = [(0, "", True)]
        while stack:
            v, prefix, last = stack.pop()
            if v == 0:
                print("0 (root)", file=sys.stderr)
            else:
                p = self.par[v]
                start = self.pos[v] + self.depth[p]
                edge = self.s[start:start + self.length[v]]
                branch = "└─ " if last else "├─ "
                mark = "*" if self.tail[v] else ""
                print(f"{prefix}{branch}{edge!r} → {v}{mark}", file=sys.stderr)
                prefix += "   " if last else "│  "

            children = self.child[v]
            last_index = len(children) - 1
            for i in range(last_index, -1, -1):
                stack.append((children[i], prefix, i == last_index))

    @staticmethod
    def _sa_is(s, upper):
        n = len(s)
        if n == 0:
            return []
        if n == 1:
            return [0]
        if n == 2:
            if s[0] < s[1]:
                return [0, 1]
            else:
                return [1, 0]
        sa = [0] * n
        ls = [0] * n
        for i in range(n - 2, -1, -1):
            ls[i] = ls[i + 1] if (s[i] == s[i + 1]) else (s[i] < s[i + 1])
        sum_l = [0] * (upper + 1)
        sum_s = [0] * (upper + 1)
        for i in range(n):
            if not (ls[i]):
                sum_s[s[i]] += 1
            else:
                sum_l[s[i] + 1] += 1
        for i in range(upper + 1):
            sum_s[i] += sum_l[i]
            if i < upper:
                sum_l[i + 1] += sum_s[i]

        def induce(lms):
            for i in range(n):
                sa[i] = -1
            buf = sum_s[:]
            for d in lms:
                if d == n:
                    continue
                sa[buf[s[d]]] = d
                buf[s[d]] += 1
            buf = sum_l[:]
            sa[buf[s[n - 1]]] = n - 1
            buf[s[n - 1]] += 1
            for i in range(n):
                v = sa[i]
                if v >= 1 and not (ls[v - 1]):
                    sa[buf[s[v - 1]]] = v - 1
                    buf[s[v - 1]] += 1
            buf = sum_l[:]
            for i in range(n - 1, -1, -1):
                v = sa[i]
                if v >= 1 and ls[v - 1]:
                    buf[s[v - 1] + 1] -= 1
                    sa[buf[s[v - 1] + 1]] = v - 1

        lms_map = [-1] * (n + 1)
        m = 0
        for i in range(1, n):
            if not (ls[i - 1]) and ls[i]:
                lms_map[i] = m
                m += 1
        lms = []
        for i in range(1, n):
            if not (ls[i - 1]) and ls[i]:
                lms.append(i)
        induce(lms)
        if m:
            sorted_lms = []
            for v in sa:
                if lms_map[v] != -1:
                    sorted_lms.append(v)
            rec_s = [0] * m
            rec_upper = 0
            rec_s[lms_map[sorted_lms[0]]] = 0
            for i in range(1, m):
                l = sorted_lms[i - 1]
                r = sorted_lms[i]
                end_l = lms[lms_map[l] + 1] if (lms_map[l] + 1 < m) else n
                end_r = lms[lms_map[r] + 1] if (lms_map[r] + 1 < m) else n
                same = True
                if end_l - l != end_r - r:
                    same = False
                else:
                    while l < end_l:
                        if s[l] != s[r]:
                            break
                        l += 1
                        r += 1
                    if (l == n) or (s[l] != s[r]):
                        same = False
                if not (same):
                    rec_upper += 1
                rec_s[lms_map[sorted_lms[i]]] = rec_upper
            del lms_map  # 縮約列の構築に使う一時配列
            rec_sa = SuffixTree._sa_is(rec_s, rec_upper)
            for i in range(m):
                sorted_lms[i] = lms[rec_sa[i]]
            induce(sorted_lms)
        return sa

    @staticmethod
    def _lcp_array(s, sa):
        n = len(s)
        if n < 2:
            return []
        rnk = [0] * n
        for i in range(n):
            rnk[sa[i]] = i
        lcp = [0] * (n - 1)
        h = 0
        for i in range(n):
            if h > 0:
                h -= 1
            if rnk[i] == 0:
                continue
            j = sa[rnk[i] - 1]
            while j + h < n and i + h < n:
                if s[j + h] != s[i + h]:
                    break
                h += 1
            lcp[rnk[i] - 1] = h
        return lcp
