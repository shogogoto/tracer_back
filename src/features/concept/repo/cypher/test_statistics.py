from ..test_nx_repo import spread_tree, narrow_tree

from . import statistics as S
from .. import relation_repo as R
from .. import Concept
from .path import Path, PathArrow
from .node import NoneNode, Node

# 関係先の数を集計
def _test_with_count_dists(spread_tree):
    g, n_map = spread_tree
    root     = g[n_map[0]]
    succ1 = list(g.G.successors(root.uid))[0]
    succ2 = list(g.G.successors(succ1))[0]
    succ3 = list(g.G.successors(succ2))[0]

    # repo = R.RelationRepo(Concept, "dests", resolved=False)
    # q    = repo.find(root.uid, None)

    arrow_to_1     = PathArrow(Concept.dests, minmax_dist=1)
    arrow_to_all   = PathArrow(Concept.dests, minmax_dist=None)
    arrow_from_1   = PathArrow(Concept.srcs, minmax_dist=1)
    arrow_from_all = PathArrow(Concept.srcs, minmax_dist=None)

    m = q.path.matched
    n = NoneNode()
    d = Node(Concept, "dest")
    s = Node(Concept, "src")
    m1 = Node(Concept, "src_tip")
    m2 = Node(Concept, "dest_tip")

    p1 = Path(arrow_to_1, m, n)
    p2 = Path(arrow_to_all, m, d)
    p3 = Path(arrow_from_1, m, n)
    p4 = Path(arrow_from_all, m, s)
    p5 = p2.tip()
    p6 = p4.tip()

    # ここのキーワード引数varが残っていてPRでエラーになっている
    c1 = S.Counter(p1, "dest1")
    c2 = S.Counter(p2, "dest_all")
    c3 = S.Counter(p3, "src1")
    c4 = S.Counter(p4, "src_all")
    d1 = S.MaxDistance(p5, "max_leaf_dist")
    d2 = S.MaxDistance(p6, "max_root_dist")
    print("######################################")
    print("######################################")

    print(p5.text)
    print(p6.text)
    print(d1.text)
    print(d2.text)
    print("######################################")
    print("######################################")
    res = q(c1, c2, c3, c4) #, d1, d2)

    _, st1 = res.filter_(uid=succ1)[0]
    _, st2 = res.filter_(uid=succ2)[0]
    _, st3 = res.filter_(uid=succ3)[0]
    assert st1 == {"dest1":2, "dest_all":6, "src1":1, "src_all": 1}
    assert st2 == {"dest1":2, "dest_all":2, "src1":1, "src_all": 2}
    assert st3 == {"dest1":0, "dest_all":0, "src1":1, "src_all": 3}

# 先端(tips)の集計
def _test_with_count_tips(narrow_tree):
    g, n_map = narrow_tree
    leaf = g[n_map[0]]

    repo = R.RelationRepo(Concept, "srcs", resolved=False)
    q    = repo.find_tips(leaf.uid)

    arrow_to_all   = PathArrow(Concept.dests, minmax_dist=(1,))
    arrow_from_all = PathArrow(Concept.srcs, minmax_dist=(1,))

    m = q.path.matched
    n1 = Node(Concept, "x")
    n2 = Node(Concept, "y")
    tip1 = Path(arrow_to_all, m, n1).tip()
    tip2 = Path(arrow_from_all, m, n2).tip()


    c1 = S.Counter(tip1, "dest_all")
    c2 = S.Counter(tip2, "src_all")

    res = q(c1, c2)
    print(q.text)
    for r in res.zip_():
        print(r)



def test_with_distance_from_tips(narrow_tree):
    pass
