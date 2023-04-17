from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from neomodel import StructuredNode, db
from . import text as T
from .path import MinMaxDistance, Path, PathFactory
from .node import Node
from .statistics import Statistics
from .result import Results


def resolve(query:str, stats_columns:list[str])->Results:
    results, columns = db.cypher_query(query, resolve_objects=True)
    return Results(results, columns, stats_columns)

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
        return self.__resolve_matched(p, uid)

    def find_tips(self, uid:str)->Results:
        p = self.factory(self.relation, None, self.matched) \
                .tip()
        return self.__resolve_matched(p, uid)

    def __resolve_matched(self, path:Path, uid:str)->T.QueryBuilder:
        b = T.QueryBuilder()
        p = T.Property(self.target.var, "uid", uid)
        w = T.Where(p.text)
        b.add_text(T.Matcher(self.target, where=w))
        b.add_text(T.Matcher(path))
        b.add_return(self.matched.var)
        self.statistics.setup(b)
        return resolve(b.text, self.statistics.columns)


@dataclass
class TargetQuery:
    label:StructuredNode
    statistics:Optional[Statistics] = Statistics()

    def __post_init__(self):
        self.target  = Node(self.label, "matched")

    def find(self, uid:str)->Results:
        b = T.QueryBuilder()
        p = T.Property(self.target.var, "uid", uid)
        w = T.Where(p.text)
        b.add_text(T.Matcher(self.target, where=w))
        b.add_return(self.target.var)
        self.statistics.setup(b)
        return resolve(b.text, self.statistics.columns)

@dataclass
class PropQuery:
    label:StructuredNode
    statistics:Optional[Statistics] = Statistics()

    def __post_init__(self):
        self.matched = Node(self.label, "matched")
        self.factory = PathFactory(self.label, self.matched)

    def find(self, key:str, value:str)->Results:
        v = f".*{value}.*"
        b = T.QueryBuilder()
        p = T.Property(self.matched.var, key, v, regex=True)
        w = T.Where(p.text)
        b.add_text(T.Matcher(self.matched, where=w))
        b.add_return(self.matched.var)
        self.statistics.setup(b)
        return resolve(b.text, self.statistics.columns)
