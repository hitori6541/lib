# Source: https://github.com/hitori6541/lib
# File: segtree/persistent_segtree.py
# Adapted from shakayami's ACL-for-python with AI assistance.
# https://info.atcoder.jp/entry/algorithm_lectures/persistent_segment_tree

class PersistentSegtree:
    """
    1 点更新・区間積を扱う完全永続セグメント木。

    初期状態のバージョン番号は 0。set, apply, copy_from は元のバージョンを
    変更せず、新しいバージョンを末尾に追加してその番号を返す。

    pst = PersistentSegtree(A, op, e)
    v1 = pst.set(0, p, x)
    value = pst.prod(v1, l, r)  # [l, r)

    構築: O(n) 時間・空間
    set, apply: O(log n) 時間・追加空間
    get, prod: O(log n) 時間
    copy_from: O(log n) 時間・追加空間
    """

    def __init__(self, V, OP, E):
        self.n = len(V)
        self.op = OP
        self.e = E
        self.left = []
        self.right = []
        self.d = []

        if self.n == 0:
            root = -1
        else:
            root = self._build(V, 0, self.n)
        # 公開するバージョン番号から、内部の根ノード番号への対応。
        self.roots = [root]

    def _new_node(self, left, right, value):
        node = len(self.d)
        self.left.append(left)
        self.right.append(right)
        self.d.append(value)
        return node

    def _build(self, V, node_l, node_r):
        if node_r - node_l == 1:
            return self._new_node(-1, -1, V[node_l])
        mid = (node_l + node_r) >> 1
        left = self._build(V, node_l, mid)
        right = self._build(V, mid, node_r)
        return self._new_node(left, right, self.op(self.d[left], self.d[right]))

    def _check_ver(self, ver):
        assert 0 <= ver and ver < len(self.roots)

    def latest_ver(self):
        """最後に生成されたバージョン番号を返す。"""
        return len(self.roots) - 1

    def set(self, ver, p, x):
        """バージョン ver の p 番目を x にし、新しいバージョン番号を返す。"""
        self._check_ver(ver)
        assert 0 <= p and p < self.n
        root = self._set(self.roots[ver], 0, self.n, p, x)
        self.roots.append(root)
        return len(self.roots) - 1

    def _set(self, node, node_l, node_r, p, x):
        if node_r - node_l == 1:
            return self._new_node(-1, -1, x)

        mid = (node_l + node_r) >> 1
        left = self.left[node]
        right = self.right[node]
        if p < mid:
            left = self._set(left, node_l, mid, p, x)
        else:
            right = self._set(right, mid, node_r, p, x)
        return self._new_node(left, right, self.op(self.d[left], self.d[right]))

    def apply(self, ver, p, f):
        """
        バージョン ver の p 番目の値 x を f(x) に変更し、
        新しいバージョン番号を返す。
        あんまり速くないのでgetしてsetしてもよい。
        """
        self._check_ver(ver)
        assert 0 <= p and p < self.n
        root = self._apply(self.roots[ver], 0, self.n, p, f)
        self.roots.append(root)
        return len(self.roots) - 1

    def _apply(self, node, node_l, node_r, p, f):
        if node_r - node_l == 1:
            return self._new_node(-1, -1, f(self.d[node]))

        mid = (node_l + node_r) >> 1
        left = self.left[node]
        right = self.right[node]
        if p < mid:
            left = self._apply(left, node_l, mid, p, f)
        else:
            right = self._apply(right, mid, node_r, p, f)
        return self._new_node(left, right, self.op(self.d[left], self.d[right]))

    def get(self, ver, p):
        """バージョン ver の p 番目の値を返す。"""
        self._check_ver(ver)
        assert 0 <= p and p < self.n
        node = self.roots[ver]
        node_l = 0
        node_r = self.n
        while node_r - node_l > 1:
            mid = (node_l + node_r) >> 1
            if p < mid:
                node = self.left[node]
                node_r = mid
            else:
                node = self.right[node]
                node_l = mid
        return self.d[node]

    def prod(self, ver, l, r):
        """バージョン ver の区間 [l, r) の積を返す。"""
        self._check_ver(ver)
        assert 0 <= l and l <= r and r <= self.n
        if l == r:
            return self.e
        return self._prod(self.roots[ver], 0, self.n, l, r)

    def _prod(self, node, node_l, node_r, l, r):
        if r <= node_l or node_r <= l:
            return self.e
        if l <= node_l and node_r <= r:
            return self.d[node]
        mid = (node_l + node_r) >> 1
        left_prod = self._prod(self.left[node], node_l, mid, l, r)
        right_prod = self._prod(self.right[node], mid, node_r, l, r)
        return self.op(left_prod, right_prod)

    def all_prod(self, ver):
        """バージョン ver の全要素の積を返す。"""
        self._check_ver(ver)
        if self.n == 0:
            return self.e
        return self.d[self.roots[ver]]

    def copy_from(self, dst_ver, src_ver, l, r):
        """
        dst_ver の [l, r) を src_ver の同一区間で置き換え、
        新しいバージョン番号を返す。
        """
        self._check_ver(dst_ver)
        self._check_ver(src_ver)
        assert 0 <= l and l <= r and r <= self.n
        if l == r:
            root = self.roots[dst_ver]
        else:
            root = self._copy_from(
                self.roots[dst_ver], self.roots[src_ver], 0, self.n, l, r
            )
        self.roots.append(root)
        return len(self.roots) - 1

    def _copy_from(self, dst, src, node_l, node_r, l, r):
        if r <= node_l or node_r <= l:
            return dst
        if l <= node_l and node_r <= r:
            return src
        mid = (node_l + node_r) >> 1
        left = self._copy_from(
            self.left[dst], self.left[src], node_l, mid, l, r
        )
        right = self._copy_from(
            self.right[dst], self.right[src], mid, node_r, l, r
        )
        return self._new_node(left, right, self.op(self.d[left], self.d[right]))
