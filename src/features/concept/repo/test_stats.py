from .cypher.test_graph import narrow_tree
from .stats_query import WithStatisticsQuery


def test_find_by_name(narrow_tree):
    g, _ = narrow_tree
    results = WithStatisticsQuery.find_by_name("source")
    assert results.names == g.prop("name")


def test_find_adjacent(narrow_tree):
    g, n_map = narrow_tree
    leaf = g[n_map[0]]
    pred_uid = list(g.G.predecessors(leaf.uid))[0]
    srcs, dests = WithStatisticsQuery.find_adjacent_by_uid(pred_uid)

    assert len(srcs) == 2
    assert len(dests) == 1
