from __future__ import annotations
from dataclasses import dataclass
from neomodel import StructuredNode, RelationshipDefinition
from . import cypher as C
from .cypher import text as T
from .cypher.path import MinMaxDistance, Path, PathArrow, PathFactory
from .cypher import Node
from typing import Union


# QueryのFactoryでもある
@dataclass
class RelationRepo:
    label:StructuredNode
    relation:str
    resolved:bool = True

    def __post_init__(self):
        self.target  = C.Node(self.label, "target")
        self.matched = C.Node(self.label, "matched")
        self.f = PathFactory(
                self.label
                , self.target)

    def find(self, uid:str, minmax_dist:MinMaxDistance)->Result:
        p = self.f(self.relation, minmax_dist, self.matched)
        return self.__resolver(p, uid)

    def find_tips(self, uid:str)->Result:
        p = self.f(self.relation, None, self.matched).tip()
        return self.__resolver(p, uid)

    def __resolver(self, path:Path, uid:str)->QueryResolver:
        s = T.QueryResolver()
        w = T.Where(self.target.var, "uid", uid)
        s.add_matcher(self.target, w)
        s.add_matcher(path)
        s.add_return(self.matched.var)
        return s() if self.resolved else s

    @property
    def rel_def(self)->RelationshipDefinition:
        return getattr(self.label, self.relation)
