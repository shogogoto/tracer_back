from ..test_nx_repo import spread_tree, narrow_tree

from . import statistics as S
from .. import relation_repo as R
from .. import Concept
from .path import Path

# 関係先の数を集計
def test_with_count_dists(spread_tree):
    g, n_map = spread_tree
    root     = g[n_map[0]]
    succ1 = list(g.G.successors(root.uid))[0]
    succ2 = list(g.G.successors(succ1))[0]
    succ3 = list(g.G.successors(succ2))[0]

    repo    = R.RelationRepo(Concept, "dests", resolved=False)
    q       = repo.find(root.uid, None)
    p = Path(Concept.dests, minmax_dist=1, source=q.path.matched, matched="n1")
    counter1 = S.Counter(p, var="dest1")
    p2 = Path(Concept.dests, minmax_dist=None, source=q.path.matched, matched="n2")
    counter2 = S.Counter(p2, var="dest_all")
    p3 = Path(Concept.srcs, minmax_dist=1, source=q.path.matched, matched="n3")
    counter3 = S.Counter(p3, var="src1")
    p4 = Path(Concept.srcs, minmax_dist=None, source=q.path.matched, matched="n4")
    counter4 = S.Counter(p4, var="src_all")

    res = q(counter1, counter2, counter3, counter4)

    _, st1 = res.filter_(uid=succ1)[0]
    _, st2 = res.filter_(uid=succ2)[0]
    _, st3 = res.filter_(uid=succ3)[0]
    assert st1 == {"dest1":2, "dest_all":6, "src1":1, "src_all": 1}
    assert st2 == {"dest1":2, "dest_all":2, "src1":1, "src_all": 2}
    assert st3 == {"dest1":0, "dest_all":0, "src1":1, "src_all": 3}

# 先端(tips)の集計
