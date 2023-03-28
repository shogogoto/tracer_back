from .graph import TripletGraph as G
from .node import ConceptNode as N
from ..repo import Concept


def test_init():
    n = N.create("trigraph","")
    srcs  = N.batch_create([(f"src{i}", f"desc{i}") for i in range(5)])
    dests = N.batch_create([(f"dst{i}", f"desc{i}") for i in range(3)])

    g = G(n, srcs=srcs, dests=dests)
    assert len(g.sources) == 5
    assert len(g.destinations) == 3
