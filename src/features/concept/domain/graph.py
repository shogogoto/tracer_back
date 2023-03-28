from __future__ import annotations

import networkx as nx
from .node import ConceptNode
from dataclasses import dataclass, InitVar


# 3段グラフ
@dataclass(frozen=True)
class TripletGraph:
    # dests: list[ConceptNode]
    center:ConceptNode
    __G: nx.DiGraph = nx.DiGraph()
    srcs: InitVar[list[ConceptNode]] = []
    dests: InitVar[list[ConceptNode]] = []

    def __post_init__(self, srcs, dests):
        c = self.center
        self.__G.add_node(c.uid, node=c.value)
        self.__add_sources(srcs)
        self.__add_destinations(dests)

    def __add_sources(self, sources):
        c = self.center
        for s in sources:
            self.__G.add_node(s.uid, node=s.value)
            self.__G.add_edge(s.uid, c.uid)

    def __add_destinations(self, destinations):
        c = self.center
        for d in destinations:
            self.__G.add_node(d.uid, node=d.value)
            self.__G.add_edge(c.uid, d.uid)

    @property
    def sources(self)->list[ConceptNode]:
        uid = self.center.uid
        src_uids = list(self.__G.predecessors(uid))
        return [
            self.__G.nodes[suid]["node"]
            for suid in src_uids
        ]

    @property
    def destinations(self)->list[ConceptNode]:
        uid = self.center.uid
        dest_uids = list(self.__G.successors(uid))
        return [
            self.__G.nodes[duid]["node"]
            for duid in dest_uids
        ]
