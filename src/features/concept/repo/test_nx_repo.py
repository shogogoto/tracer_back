from .nx_repo import NeoDiGraph as ND
from . import Concept

import networkx as nx

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
    print(c1.dests.get())

def test_nx_digraph_wapped():
    g = ND(Concept)
    k1 = g.add_node(name="nd1")
    k2 = g.add_node(name="nd2")
    g.add_edge(k1, k2)

    assert g[k1] == Concept.nodes.first(name="nd1")
    assert g[k2] == Concept.nodes.first(name="nd2")
    assert g[k2] == g[k1].dests.get()


def test_search_source():
    # g = ND(Concept)
    # c1 = g.add_node(name="1th")
    # ss0 = [g.add_source     (c1, name=f"s0{i}") for i in range(5)]
    # ds0 = [g.add_destination(c1, name=f"d0{i}") for i in range(4)]
    # c2 = ds0[0]
    # ss1 = [g.add_source     (c2, name=f"s1{i}") for i in range(5)]
    # ds1 = [g.add_destination(c2, name=f"d1{i}") for i in range(3)]

    # c3 = ds1[0]
    # ss2 = [g.add_source     (c3, name=f"s2{i}") for i in range(5)]
    # ds2 = [g.add_destination(c3, name=f"d2{i}") for i in range(3)]

    # c4 = ds2[0]
    # ss3 = [g.add_source     (c4, name=f"s3{i}") for i in range(5)]
    # ds2 = [g.add_destination(c4, name=f"d3{i}") for i in range(3)]

    tree = nx.balanced_tree(3, 3, nx.DiGraph())
    nx.set_node_attributes(tree, name="name", values={ n: f"name{n}" for n in tree.nodes})
    g, n_map = ND.of(Concept, tree)
    # rtree = nx.reverse(tree)
    # h, m2 = ND.of(Concept, rtree)
    # root_id = tree[n_map[0]]
    root = g[n_map[0]]
    print(root)
    print(n_map)

    # print(set(g.G.successors(root.id)))
    # print(g.G.successors(root.id))
    # uniq = Q.UniqIdMatcher(Concept, root.uid)
    # print(uniq)
    # sq = Q.SourceConfig(min_dist=1, max_dist=1)
    # dq = Q.DestinationConfig(min_dist=1, max_dist=2)
    # g.G.predecessors(n)
