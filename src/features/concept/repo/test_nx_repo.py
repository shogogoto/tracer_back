import pytest
from .nx_repo import NeoDiGraph as ND
from . import Concept

import networkx as nx

from . import statistics_query as Q
from functools import reduce


# テスト用グラフ作成ユーティリティ
def test_create_graph():
    # g = G(Concept)
    g = nx.DiGraph()
    g.add_node(1, name="nx1")
    g.add_node(2, name="nx2")
    g.add_edge(1, 2)

    ND.of(Concept, g)

    c1 = Concept.nodes.first(name="nx1")
    c2 = Concept.nodes.first(name="nx2")
    assert c1
    assert c2 == c1.dests.get()

def test_nx_digraph_wapped():
    g = ND(Concept)
    k1 = g.add_node(name="nd1")
    k2 = g.add_node(name="nd2")
    g.add_edge(k1, k2)

    assert g[k1] == Concept.nodes.first(name="nd1")
    assert g[k2] == Concept.nodes.first(name="nd2")
    assert g[k2] == g[k1].dests.get()


# 1階、2階、3階の関係元を取得
def test_find_source():
    tree = nx.balanced_tree(2, 3, nx.DiGraph())
    tree = nx.reverse(tree)
    nx.set_node_attributes(tree, name="name",
        values={ n: f"test_source{n}" for n in tree.nodes})
    g, n_map = ND.of(Concept, tree)
    leaf = g[n_map[0]]
    pred1 = set(g.G.predecessors(leaf.uid))
    pred2 = reduce(set.union, [set(g.G.predecessors(n)) for n in pred1])
    pred3 = reduce(set.union, [set(g.G.predecessors(n)) for n in pred2])

    repo = Q.RelationRepo(Concept, "srcs")
    result1  = repo.find(leaf.uid, 1, 1)
    result2  = repo.find(leaf.uid, 2, 2)
    result3  = repo.find(leaf.uid, 3, 3)
    result23 = repo.find(leaf.uid, 2, 3)

    assert pred1 == result1.uids
    assert pred2 == result2.uids
    assert pred3 == result3.uids
    assert pred2.union(pred3) == result23.uids

    # with pytest.raises(Exception) as e:
    #     Q.RelationRepo.find(root.uid, 3, 2)

# 1階、2階、3階の関係先を取得
def test_find_destinations():
    tree = nx.balanced_tree(2, 3, nx.DiGraph())
    nx.set_node_attributes(tree, name="name",
        values={ n: f"test_dest{n}" for n in tree.nodes})
    g, n_map = ND.of(Concept, tree)
    root = g[n_map[0]]
    succ1 = set(g.G.successors(root.uid))
    succ2 = reduce(set.union, [set(g.G.successors(n)) for n in succ1])
    succ3 = reduce(set.union, [set(g.G.successors(n)) for n in succ2])

    repo = Q.RelationRepo(Concept, "dests")
    result1  = repo.find(root.uid, 1, 1)
    result2  = repo.find(root.uid, 2, 2)
    result3  = repo.find(root.uid, 3, 3)
    result23 = repo.find(root.uid, 2, 3)

    assert succ1 == result1.uids
    assert succ2 == result2.uids
    assert succ3 == result3.uids
    assert succ2.union(succ3) == result23.uids
