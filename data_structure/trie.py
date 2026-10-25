
from collections import deque
class Trie:
    """
    Node, dfsなどは適宜設計して使う
    -Ahoなし
    ABC403E-Forbidden Prefix; ABC437E-Sort Arrays;
    -Ahoあり
    ABC419F-All Included; ABC458F-Critical Misread
    """
    class Node:
        def __init__(self, par):
            self.par = par
            self.child = {} #{label:node_id}
            self.array = set() #ここを終点とする列のidxが入る

    def __init__(self):
        self.nodes = [self.Node(-1)]
        self.i2id = {0:0} #文字列のidx -> 頂点番号
        # 以下Aho用
        self.fail = None
        self.bfs_order = None

    def add_array(self, s, i):
        #i:列のidx は1-indexedにすべし
        now = 0
        for c in s:
            if c not in self.nodes[now].child:
                nxt_id = len(self.nodes)
                self.nodes.append(self.Node(now))
                self.nodes[now].child[c] = nxt_id
            now = self.nodes[now].child[c]
        self.nodes[now].array.add(i)
        self.i2id[i] = now
        return now
    
    def add_point(self, par_id, c, i):
        if c not in self.nodes[par_id].child:
            nxt_id = len(self.nodes)
            self.nodes.append(self.Node(par_id))
            self.nodes[par_id].child[c] = nxt_id
        child_id = self.nodes[par_id].child[c]
        self.nodes[child_id].array.add(i)
        self.i2id[i] = child_id
        return child_id
    
    def dfs(self, start_id):
        #ラベルの辞書順に探索するだけ　色々足して使う
        q = [start_id]
        while q:
            v1 = q.pop()
            for label2 in sorted(self.nodes[v1].child.keys(), reverse=True):
                v2 = self.nodes[v1].child[label2]
                q.append(v2)
        return
    
    def bfs(self, start_id):
        q = deque([start_id])
        while q:
            v1 = q.popleft()
            for label2, v2 in self.nodes[v1].child.items():
                q.append(v2)
    
    def build_failure_link(self):
        """
        Aho-Corasick の failure link を構築する。
        注意：この関数を呼んだ後に add_array/add_point で trie を拡張したら fail/out は作り直し。
        便利なのでTrieのBFS順も持っておく
        """
        n = len(self.nodes)
        fail = [0] * n
        q = deque()
        order = [0]  
        for c, nxt in self.nodes[0].child.items(): # root の子は fail=0
            fail[nxt] = 0
            q.append(nxt)
        while q:
            v = q.popleft()
            order.append(v)
            for c, u in self.nodes[v].child.items():
                q.append(u)
                f = fail[v]
                while f != 0 and c not in self.nodes[f].child:
                    f = fail[f]
                if c in self.nodes[f].child:
                    fail[u] = self.nodes[f].child[c]
                else:
                    fail[u] = 0
        self.fail = fail
        self.bfs_order = order

    def build_Aho_graph(self,words="abcdefghijklmnopqrstuvwxyz"):
        """
        頂点iから文字cを使ったら頂点jに行く ret[i][c] = j
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        """
        n = len(self.nodes)
        m = len(words)
        ret = [[0]*m for _ in range(n)]
        for v in self.bfs_order:
            for k, c in enumerate(words):
                if c in self.nodes[v].child:
                    ret[v][k] = self.nodes[v].child[c]
                elif v == 0:
                    ret[v][k] = 0
                else:
                    ret[v][k] = ret[self.fail[v]][k]
        return ret
    
    def Aho_denpa(self):
        """
        終点フラグをFailureからもらう
        """
        for v in self.bfs_order:
            self.nodes[v].array |= self.nodes[self.fail[v]].array