from __future__ import annotations
from dataclasses import dataclass
from neomodel import StructuredNode, RelationshipDefinition
from . import cypher as C
from .cypher import text as T
from .cypher.path import MinMaxDistance, Path, PathArrow
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

    def find(self, uid:str, minmax_dist:MinMaxDistance)->Result:
        p = C.PathArrow(self.rel_def, minmax_dist) \
             .to_path(self.target, self.matched)
        return self.__resolver(p, uid)

    def find_tips(self, uid:str)->Result:
        p = C.PathArrow(self.rel_def, None) \
             .to_path(self.target, self.matched) \
             .tip()
        return self.__resolver(p, uid)

    def __resolver(self, path:Path, uid:str)->QueryResolver:
        s = T.QueryResolver()
        s.add_matcher(self.target.with_where("uid", uid))
        s.add_matcher(path.text)
        s.add_return(self.matched.var)
        return s() if self.resolved else s

    @property
    def rel_def(self)->RelationshipDefinition:
        return getattr(self.label, self.relation)
