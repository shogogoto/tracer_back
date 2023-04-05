from ..test_nx_repo import spread_tree, narrow_tree

from . import statistics as S
from .. import relation_repo as R
from .. import Concept
from .path import Path, PathArrow
from .node import NoneNode

# 関係先の数を集計
def test_with_count_dists(spread_tree):
    g, n_map = spread_tree
    root     = g[n_map[0]]
    succ1 = list(g.G.successors(root.uid))[0]
    succ2 = list(g.G.successors(succ1))[0]
    succ3 = list(g.G.successors(succ2))[0]

    repo    = R.RelationRepo(Concept, "dests", resolved=False)
    q       = repo.find(root.uid, None)

    arrow_to_1     = PathArrow(Concept.dests, minmax_dist=1)
    arrow_to_all   = PathArrow(Concept.dests, minmax_dist=None)
    arrow_from_1   = PathArrow(Concept.srcs, minmax_dist=1)
    arrow_from_all = PathArrow(Concept.srcs, minmax_dist=None)

    m = q.path.matched
    n = NoneNode()
    p1 = Path(arrow_to_1, m, n)
    p2 = Path(arrow_to_all, m, n)
    p3 = Path(arrow_from_1, m, n)
    p4 = Path(arrow_from_all, m, n)

    c1 = S.Counter(p1, var="dest1")
    c2 = S.Counter(p2, var="dest_all")
    c3 = S.Counter(p3, var="src1")
    c4 = S.Counter(p4, var="src_all")
    res = q(c1, c2, c3, c4)

    _, st1 = res.filter_(uid=succ1)[0]
    _, st2 = res.filter_(uid=succ2)[0]
    _, st3 = res.filter_(uid=succ3)[0]
    assert st1 == {"dest1":2, "dest_all":6, "src1":1, "src_all": 1}
    assert st2 == {"dest1":2, "dest_all":2, "src1":1, "src_all": 2}
    assert st3 == {"dest1":0, "dest_all":0, "src1":1, "src_all": 3}

# 先端(tips)の集計
