from ..test_nx_repo import spread_tree, narrow_tree

from . import statistics as S
from .. import relation_repo as R
from .. import Concept
from .path import Path, PathArrow, PathFactory
from .node import NoneNode, Node
from .result import Results

from neomodel import db

# 関係先の数を集計
def test_with_count_dists(spread_tree):
    g, n_map = spread_tree
    root     = g[n_map[0]]
    succ1 = list(g.G.successors(root.uid))[0]
    succ2 = list(g.G.successors(succ1))[0]
    succ3 = list(g.G.successors(succ2))[0]

    repo = R.RelationRepo(Concept, "dests", resolved=False)
    qb   = repo.find(root.uid, None)

    n  = Node(Concept, "")
    n1 = Node(Concept, "n1")
    n2 = Node(Concept, "n2")
    n3 = Node(Concept, "n3")
    n4 = Node(Concept, "n4")
    m1 = Node(Concept, "dest_matched")
    m2 = Node(Concept, "src_matched")
    f  = PathFactory(Concept, repo.matched)
    p1 = f("dests", 1,    n)
    p2 = f("dests", None, n2)
    p3 = f("srcs", 1,     n3)
    p4 = f("srcs", None,  n4)
    tip1 = f("dests", None, m1).tip()
    tip2 = f("srcs", None, m2).tip()

    s = S.Statistics(qb) \
        .counted(p1, "dest1") \
        .counted(p2, "dest_all") \
        .counted(p3, "src1") \
        .counted(p4, "src_all") \
        .distanced(tip1, "leaf_dist") \
        .distanced(tip2, "root_dist")

    print("##################################")
    print(qb.text)
    print()
    results, columns = db.cypher_query(qb.text, resolve_objects=True)
    res = Results(results, columns, s.columns)
    stats = res.statistics()
    uids = res.column_attrs("matched", "uid")
    i1   = uids.index(succ1)
    i2   = uids.index(succ2)
    i3   = uids.index(succ3)

    expected1 = {"dest1":2, "dest_all":6, "src1":1, "src_all": 1
                 ,"leaf_dist": 2.0, "root_dist": 1.0}
    expected2 = {"dest1":2, "dest_all":2, "src1":1, "src_all": 2
                 ,"leaf_dist": 1.0, "root_dist": 2.0}
    expected3 = {"dest1":0, "dest_all":0, "src1":1, "src_all": 3
                 ,"leaf_dist": 0.0, "root_dist": 3.0}
    assert stats[i1] == expected1
    assert stats[i2] == expected2
    assert stats[i3] == expected3

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
