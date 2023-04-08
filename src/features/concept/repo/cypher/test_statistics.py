from ..test_nx_repo import spread_tree, narrow_tree

from . import statistics as S
from .. import relation_repo as R
from .. import Concept
from .path import Path, PathArrow, PathFactory
from .node import NoneNode, Node
from .result import Results

from neomodel import db

# 関係先の数を集計
def _test_with_count_dists(spread_tree):
    g, n_map = spread_tree
    root     = g[n_map[0]]
    succ1 = list(g.G.successors(root.uid))[0]
    succ2 = list(g.G.successors(succ1))[0]
    succ3 = list(g.G.successors(succ2))[0]

    repo = R.RelationRepo(Concept, "dests")

    n  = Node(Concept, "")
    m1 = Node(Concept, "dest_matched")
    m2 = Node(Concept, "src_matched")
    f  = PathFactory(Concept, repo.matched)
    p1 = f("dests", 1,    n)
    p2 = f("dests", None, n)
    p3 = f("srcs", 1,     n)
    p4 = f("srcs", None,  n)
    tip1 = f("dests", None, m1).tip()
    tip2 = f("srcs", None, m2).tip()

    repo.statistics = S.Statistics() \
        .counted(p1, "dest1") \
        .counted(p2, "dest_all") \
        .counted(p3, "src1") \
        .counted(p4, "src_all") \
        .distanced(tip1, "leaf_dist") \
        .distanced(tip2, "root_dist")

    repo.find(root.uid, None)
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
