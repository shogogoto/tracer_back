from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from neomodel import StructuredNode, db
from . import text as T
from .path import MinMaxDistance, Path, PathFactory
from . import Node
from .statistics import Statistics
from .result import Results

# QueryのFactoryでもある
@dataclass
class RelationQuery:
    label:StructuredNode
    relation:str
    statistics:Optional[Statistics] = Statistics()

    def __post_init__(self):
        self.target  = Node(self.label, "target")
        self.matched = Node(self.label, "matched")
        self.factory = PathFactory(self.label, self.target)

    def find(self, uid:str, minmax_dist:MinMaxDistance)->Results:
        p = self.factory(self.relation, minmax_dist, self.matched)
        return self.__resolve(p, uid)

    def find_tips(self, uid:str)->Results:
        p = self.factory(self.relation, None, self.matched) \
                .tip()
        return self.__resolve(p, uid)

    def __resolve(self, path:Path, uid:str)->T.QueryBuilder:
        b = T.QueryBuilder()
        w = T.Where(self.target.var, "uid", uid)
        b.add_text(T.Matcher(self.target, where=w))
        b.add_text(T.Matcher(path))
        b.add_return(self.matched.var)

        self.statistics.setup(b)

        results, columns = db.cypher_query(b.text, resolve_objects=True)
        res = Results(results, columns, self.statistics.columns)
        return res

