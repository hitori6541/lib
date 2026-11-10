# ファイル一覧
非公開にした実装は、参考用に出典へのリンクを残しています。

## data_structure

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [bit_set.py](data_structure/bit_set.py) | o | AI / [提出](https://atcoder.jp/contests/abc147/submissions/73870031) |
| [interval_set.py](data_structure/interval_set.py) | o | IntervalSet: AI / SortedSet: tatyam-prime (Unlicense、出典はコード内) |
| [sorted_multiset.py](data_structure/sorted_multiset.py) | x | https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py |
| [sorted_set.py](data_structure/sorted_set.py) | x | https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py |
| [sparse_table.py](data_structure/sparse_table.py) | x | https://judge.yosupo.jp/submission/264467 |
| [swag.py](data_structure/swag.py) | x | https://qiita.com/Shirotsume/items/4a2837b5895ef9a7aeb1 |
| [trie.py](data_structure/trie.py) | o | AI |
| [wavelet_matrix.py](data_structure/wavelet_matrix.py) | x | https://judge.yosupo.jp/submission/151722 |

## geometry

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [memo_geo.md](geometry/memo_geo.md) | o |  |
| [affine_2D.py](geometry/affine_2D.py) | o |  |
| [henkakusort.py](geometry/henkakusort.py) | o | 参考: https://blog.ngtkana.com/entry/2021/11/13/202103 |
| [line.py](geometry/line.py) | o | AI / [提出](https://atcoder.jp/contests/abc467/submissions/80536497) |
| [totsuhou.py](geometry/totsuhou.py) | x | https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain |
| [vec.py](geometry/vec.py) | o | AI |

## graph

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [bipartite_matching.py](graph/bipartite_matching.py) | x | https://judge.yosupo.jp/submission/226131 |
| [cycle_detect.py](graph/cycle_detect.py) | x | https://judge.yosupo.jp/submission/143782 https://judge.yosupo.jp/submission/143632|
| [max_flow.py](graph/max_flow.py) | x | [実装元](https://github.com/shakayami/ACL-for-python/blob/master/maxflow.py) (Unlicense) / [解説メモの参照元](https://yosupo.hatenablog.com/entry/2015/03/31/134336) |
| [scc.py](graph/scc.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/scc.py |
| [union_find_linear.py](graph/union_find_linear.py) | x | https://zenn.dev/luna_moonlight/articles/d02d85532becd3 |
| [union_find_weighted.py](graph/union_find_weighted.py) | o | 自作 / AI |
| [union_find.py](graph/union_find.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/dsu.py |
| [ushi_game.py](graph/ushi_game.py) | o | 自作 |
| [ushi_game.md](graph/ushi_game.md) | o | 自作 / 差分制約のメモ |

## math

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [memo_bit_tricks.md](math/memo_bit_tricks.md) | o |  |
| [crt.py](math/crt.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/acl_math.py |
| [eratos.py](math/eratos.py) | o | AI |
| [ext_gcd.py](math/ext_gcd.py) | o | AI |
| [fft.py](math/fft.py) | x | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/convolution.py |
| [fps_notes.md](math/fps_notes.md) | o | 母関数メモ・FPS補助関数 |
| [matrix.py](math/matrix.py) | o | AI |
| [comb.py](math/comb.py) | o | AI / 参考資料はコード内 |
| [comb_table.py](math/comb_table.py) | o | 自作 |

## optimization

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [monotone_cht.py](optimization/monotone_cht.py) | o | 自作 / AI / [提出（Frog 3）](https://atcoder.jp/contests/dp/submissions/80750378) |

## segtree

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [monoid4lazysegtree.md](segtree/monoid4lazysegtree.md) | o | |
| [monoid4segtree.md](segtree/monoid4segtree.md) | o | 検証用の提出リンクは本文内 |
| [fenwick_tree.py](segtree/fenwick_tree.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/fenwicktree.py |
| [fenwick_tree_mod.py](segtree/fenwick_tree_mod.py) | o | shakayami (Unlicense、出典はコード内) |
| [fenwick_tree_dual.py](segtree/fenwick_tree_dual.py) | o | fenwick_tree.py から分離（分割元の出典はコード内） |
| [fenwick_tree_rars.py](segtree/fenwick_tree_rars.py) | o | shakayami由来・AI改変 (Unlicense、出典はコード内) |
| [lazy_segtree.py](segtree/lazy_segtree.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/lazysegtree.py |
| [persistent_segtree.py](segtree/persistent_segtree.py) | o | shakayami由来・AI改変 (Unlicense、出典はコード内) |
| [segtree.py](segtree/segtree.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/segtree.py |
| [segtree_beats.py](segtree/segtree_beats.py) | x | https://judge.yosupo.jp/submission/192936 |

## sequence

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [imos.py](sequence/imos.py) | o | AI |
| [tentou.py](sequence/tentou.py) | o | 転倒数 / fenwick_tree.py から分離 |
| [lis.py](sequence/lis.py) | o | HUMAN |
| [merge_sort.py](sequence/merge_sort.py) | o | AI |
| [mo.py](sequence/mo.py) | x | https://atcoder.jp/contests/abc242/submissions/54739420 |
| [prefix_sum_1d.py](sequence/prefix_sum/prefix_sum_1d.py) | o | AI |
| [prefix_sum_1d_mod.py](sequence/prefix_sum/prefix_sum_1d_mod.py) | o | AI |
| [prefix_sum_2d.py](sequence/prefix_sum/prefix_sum_2d.py) | o | AI |
| [prefix_sum_2d_mod.py](sequence/prefix_sum/prefix_sum_2d_mod.py) | o | AI |
| [prefix_xor_2d.py](sequence/prefix_sum/prefix_xor_2d.py) | o | AI |
| [prefix_sum_nd.py](sequence/prefix_sum/prefix_sum_nd.py) | o | AI / [提出](https://atcoder.jp/contests/abc465/submissions/77234011) |
| [zaatu.py](sequence/zaatu.py) | o | AI |

## string

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [rolling_hash.py](string/rolling_hash.py) | o | AI |
| [z_algorithm.py](string/z_algorithm.py) | o | shakayami (Unlicense): https://github.com/shakayami/ACL-for-python/blob/master/acl_string.py |

## tree

| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [tree_diameter.py](tree/tree_diameter.py) | o | AI / [提出](https://atcoder.jp/contests/abc482/submissions/80535690) |
| [find_jushin.py](tree/find_jushin.py) | o | 参考: https://atcoder.jp/contests/abc291/editorial/5840 |
| [cartesian_tree.py](tree/cartesian_tree.py) | x | https://judge.yosupo.jp/submission/143878 |
| [euler_tour.py](tree/euler_tour.py) | o | AI |
| [heavy_light_decomposition.py](tree/heavy_light_decomposition.py) | x | https://judge.yosupo.jp/submission/213447 |
| [prufer_code.py](tree/prufer_code.py) | o | 自作 / 参考資料はコード内 / [提出](https://yukicoder.me/submissions/1196599) |
| [zenhoui_kidp.py](tree/zenhoui_kidp.py) | x | [元記事](https://qiita.com/Kiri8128/items/a011c90d25911bdb3ed3)のコードを改変・再配布条件未確認 / [現行版の提出](https://atcoder.jp/contests/njpc2017/submissions/80536365) |

## root
| ファイル | 公開 | 備考 |
| --- | :---: | --- |
| [.gitignore](.gitignore) | o | |
| [README.md](README.md) | o | |
| [LICENSE](LICENSE) | o | The Unlicense |
| [AGENTS.md](AGENTS.md) | x | |
| [HUMAN.md](HUMAN.md) | x | |
| [CATALOG.md](CATALOG.md) | o | |
| [INDEX.md](INDEX.md) | x | ローカル用のファイル一覧 |
| [TODO.md](TODO.md) | x | 人間向けの整備タスク |
| [DIARY.md](DIARY.md) | x | 人間向けの整備記録 |
