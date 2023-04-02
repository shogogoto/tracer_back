from dataclasses import dataclass
from neomodel import (
        StructuredNode
        , StructuredRel
        , db
        , RelationshipDefinition
        )
from typing import Union, Optional, Callable, Hashable
from abc import ABC, abstractmethod
from . import Concept


class CypherText(ABC):
    @abstractmethod
    def build(self)->str:
        pass

    @property
    def text(self)->str:
        return self.build()


@dataclass(frozen=True)
class UniqIdNode(CypherText):
    label:StructuredNode
    uid:Hashable
    var:str = "target"

    def build(self)->str:
        labs = ":".join(self.label.inherited_labels())
        v    = self.var
        return f"({v}:{labs}) WHERE {v}.uid = '{self.uid}'"


@dataclass(frozen=True)
class Path(CypherText):
    rel:RelationshipDefinition
    min_dist:int
    max_dist:int
    source:str
    var:str = "p"

    def build(self)->str:
        rel_def = self.rel.definition
        t = rel_def["relation_type"]
        labels = rel_def["node_class"].inherited_labels()
        ls = ":".join(labels)
        s = self.source
        arrow = f"-[rel:{t}*{self.min_dist}..{self.max_dist}]->"
        if self.direction == 1:
            return f"{self.var} = ({s}){arrow}(dest:{ls})"
        elif self.direction == -1:
            return f"{self.var} = (src:{ls}){arrow}({s})"
        else:
            raise ValueError("なんかdirectionは±1以外にもあるらしい")

    @property
    def direction(self)->int:
        return self.rel.definition["direction"]

    @property
    def result_index(self)->int:
        if self.direction == 1:
            return -1
        else:
            return 0


# # 関係(edge)の統計情報
# @dataclass(frozen=True)
# class PathCounter:
#     pass


@dataclass(frozen=True)
class RelationRepo:
    label:StructuredNode
    relation:str

    def find(self, uid:str, min_dist=1, max_dist=1):
        uniq = UniqIdNode(self.label, uid)
        rel = getattr(self.label, self.relation)
        p = Path(rel, min_dist, max_dist, source=uniq.var)
        query = f"""
            MATCH {uniq.text}
            MATCH {p.text}
            RETURN nodes({p.var})
        """
        # print(query)
        params = {"uid": uid}
        results, columns = db.cypher_query(
                query
                , params=params
                , resolve_objects=True)
        resolved = [r[0][0][p.result_index] for r in results]
        return Result(resolved, columns)


@dataclass(frozen=True)
class Result:
    resolved:list[StructuredNode]
    params:dict[str]

    @property
    def uids(self)->set[str]:
        return set([r.uid for r in self.resolved])


    #     query = """
    #         MATCH (start:Concept) WHERE start.uid = $uid
    #         WITH start
    #         MATCH p = (start)-[rel:INFER*]->(src:Concept)
    #         RETURN
    #             src
    #             , COUNT {(src)-[:INFER]->(tmp:Concept)} as cnt_dests
    #             , COUNT {(src)-[:INFER*2]->(tmp:Concept)} as cnt_dests_ord2
    #             , length(p) as distance
    #     """
    #     results, columns = db.cypher_query(query, params={"uid": uid}, resolve_objects=True)
    #     # return [Concept.inflate(r[0]) for r in results]
