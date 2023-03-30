from __future__ import annotations
from typing import TypeVar, Generic, Hashable
from dataclasses import dataclass, InitVar
from uuid import uuid4

from neomodel import StructuredNode, db
import networkx as nx
from . import Concept

@dataclass(frozen=False)
class NeoDiGraph:
    label:StructuredNode
    __G:nx.DiGraph = nx.DiGraph()

    def add_node(self, **kwargs)->Hashable:
        l = self.label(**kwargs).save()
        self.__G.add_node(l.id, node=l)
        return l.id # uidは全てのlabelが持つ

    def add_edge(self,
            n_start:Hashable,
            n_end:Hashable
            ):
            s = self[n_start]
            e = self[n_end]
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
        return self.__G.nodes[n]["node"]

    @classmethod
    def of(cls,
           label:StructuredNode,
           g:nx.DiGraph
        )->NeoDiGraph:
        self = cls(label)

        models = label.create_or_update(
            *[g.nodes[n] for n in g.nodes])
        n_map = {
            n: models[i].id
            for i, n in enumerate(g.nodes)
        }
        for m in models:
            self.__G.add_node(m.id, node=m)

        for n_start, n_end in g.edges:
            s = n_map[n_start]
            e = n_map[n_end]
            self.add_edge(s, e)
        return self, n_map
