from __future__ import annotations
from typing import Hashable
from dataclasses import dataclass, InitVar

from neomodel import StructuredNode
import networkx as nx


@dataclass(frozen=False)
class NeoDiGraph:
    # StructuredNodeではなく、
    #  uidをもつことを保証するBaseNodeを定義すべきか
    label:StructuredNode
    G:nx.DiGraph = nx.DiGraph()

    def add_node(self, **kwargs)->Hashable:
        l = self.label(**kwargs).save()
        self.G.add_node(l.uid, node=l)
        return l.uid # uidは全てのlabelが持つ

    def add_edge(self,
            n_start:Hashable,
            n_end:Hashable
            ):
            s = self[n_start]
            e = self[n_end]
            self.G.add_edge(n_start, n_end)
            s.dests.connect(e)

    def add_source(self, n:Hashable, **kwargs)->Hashable:
        n_added = self.add_node(**kwargs)
        self.add_edge(n_added, n)
        return n_added

    def add_destination(self, n:Hashable, **kwargs)->Hashable:
        n_added = self.add_node(**kwargs)
        self.add_edge(n, n_added)
        return n_added


    def __getitem__(self, n)->StructuredNode:
        return self.G.nodes[n]["node"]

    @classmethod
    def of(cls,
           label:StructuredNode,
           g:nx.DiGraph
        )->tuple[NeoDiGraph,dict[Hashable,Hashable]]:
        self = cls(label)

        models = label.create_or_update(
            *[g.nodes[n] for n in g.nodes]
        )

        n_map = {
            n: models[i].uid
            for i, n in enumerate(g.nodes)
        }
        for m in models:
            self.G.add_node(m.uid, node=m)

        for n_start, n_end in g.edges:
            s = n_map[n_start]
            e = n_map[n_end]
            self.add_edge(s, e)
        return self, n_map
