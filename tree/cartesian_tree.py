# Source: https://github.com/hitori6541/lib
# File: tree/cartesian_tree.py
# Submit: https://judge.yosupo.jp/submission/416980
# Reference: https://drken1215.hatenablog.com/entry/2023/10/19/025800

def cartesian_tree(a: list) -> tuple[int, list[int], list[int]]:
    """最小カルテシアン木を構築し、(root, left, right) を返す。

    頂点番号は a の添字。各区間の分割点は一番左の最小値の位置。
    left[i], right[i] は左右の子の番号で、子がなければ -1。
    空入力では (-1, [], []) を返す。時間・空間ともに O(N)。
    """
    n = len(a)
    left = [-1] * n
    right = [-1] * n
    stack = []
    for i in range(n):
        # スタックは根から右の子だけをたどった経路。
        last = -1
        while stack and a[i] < a[stack[-1]]:
            last = stack.pop()
        left[i] = last
        if stack:
            right[stack[-1]] = i
        stack.append(i)

    root = stack[0] if stack else -1
    return root, left, right
