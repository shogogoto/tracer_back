import pytest
from .graph import NeoDiGraph as ND
from .. import Concept
import networkx as nx
from . import facade as Q
from functools import reduce, cache


# テスト用グラフ作成ユーティリティ
def test_create_graph():
    g = nx.DiGraph()
    g.add_node(1, name="nx1")
    g.add_node(2, name="nx2")
    g.add_edge(1, 2)

    ND.of(Concept, g)

    c1 = Concept.nodes.first(name="nx1")
    c2 = Concept.nodes.first(name="nx2")
    assert c1
    assert c2 == c1.dests.get()

def test_create_graph_by_wapped():
    g = ND(Concept)
    k1 = g.add_node(name="nd1")
    k2 = g.add_node(name="nd2")
    g.add_edge(k1, k2)

    assert g[k1] == Concept.nodes.first(name="nd1")
    assert g[k2] == Concept.nodes.first(name="nd2")
    assert g[k2] == g[k1].dests.get()


@pytest.fixture
@cache
def narrow_tree(): #内向き
    pass
    tree = nx.balanced_tree(2, 3, nx.DiGraph())
    tree = nx.reverse(tree)
    nx.set_node_attributes(tree, name="name",
        values={ n: f"test_source{n}" for n in tree.nodes})
    return ND.of(Concept, tree)

@pytest.fixture
@cache
def spread_tree(): # 外向き
    tree = nx.balanced_tree(2, 3, nx.DiGraph())
    nx.set_node_attributes(tree, name="name",
        values={ n: f"test_dest{n}" for n in tree.nodes})
    return ND.of(Concept, tree)

# 1階、2階、3階の関係元を取得
def test_find_source(narrow_tree):
    g, n_map = narrow_tree
    leaf = g[n_map[0]]
    pred1 = set(g.G.predecessors(leaf.uid))
    pred2 = reduce(set.union, [set(g.G.predecessors(n)) for n in pred1])
    pred3 = reduce(set.union, [set(g.G.predecessors(n)) for n in pred2])

    repo = Q.RelationQuery(Concept, "srcs")
    result1  = repo.find(leaf.uid, 1)
    result2  = repo.find(leaf.uid, 2)
    result3  = repo.find(leaf.uid, 3)
    result23 = repo.find(leaf.uid, (2, 3))

    assert pred1 == result1.uids
    assert pred2 == result2.uids
    assert pred3 == result3.uids
    assert pred2.union(pred3) == result23.uids


# 1階、2階、3階の関係先を取得
def test_find_destinations(spread_tree):
    g, n_map = spread_tree
    root = g[n_map[0]]
    succ1 = set(g.G.successors(root.uid))
    succ2 = reduce(set.union, [set(g.G.successors(n)) for n in succ1])
    succ3 = reduce(set.union, [set(g.G.successors(n)) for n in succ2])

    repo = Q.RelationQuery(Concept, "dests")
    result1  = repo.find(root.uid, 1)
    result2  = repo.find(root.uid, 2)
    result3  = repo.find(root.uid, 3)
    result23 = repo.find(root.uid, (2, 3))

    assert succ1 == result1.uids
    assert succ2 == result2.uids
    assert succ3 == result3.uids
    assert succ2.union(succ3) == result23.uids

def test_find_roots(narrow_tree):
    g, n_map = narrow_tree
    leaf = g[n_map[0]]

    pred1 = list(g.G.predecessors(leaf.uid))[0]
    pred2 = list(g.G.predecessors(pred1))[0]
    pred3 = list(g.G.predecessors(pred2))[0]

    repo = Q.RelationQuery(Concept, "srcs")
    tips1 = repo.find(leaf.uid, 3)
    tips2 = repo.find(pred1, 2)
    tips3 = repo.find(pred2, 1)
    tips4 = repo.find(pred3, 1)
    result1 = repo.find_tips(leaf.uid)
    result2 = repo.find_tips(pred1)
    result3 = repo.find_tips(pred2)
    result4 = repo.find_tips(pred3)

    assert tips1.uids == result1.uids
    assert tips2.uids == result2.uids
    assert tips3.uids == result3.uids
    assert tips4.uids == result4.uids


def test_find_leaves(spread_tree):
    g, n_map = spread_tree
    root = g[n_map[0]]

    succ1 = list(g.G.successors(root.uid))[0]
    succ2 = list(g.G.successors(succ1))[0]
    succ3 = list(g.G.successors(succ2))[0]

    repo = Q.RelationQuery(Concept, "dests")
    tips1 = repo.find(root.uid, 3)
    tips2 = repo.find(succ1, 2)
    tips3 = repo.find(succ2, 1)
    tips4 = repo.find(succ3, 1)
    result1 = repo.find_tips(root.uid)
    result2 = repo.find_tips(succ1)
    result3 = repo.find_tips(succ2)
    result4 = repo.find_tips(succ3)

    assert tips1.uids == result1.uids
    assert tips2.uids == result2.uids
    assert tips3.uids == result3.uids
    assert tips4.uids == result4.uids
