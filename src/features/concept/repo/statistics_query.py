from __future__ import annotations
from dataclasses import dataclass
from neomodel import (
        StructuredNode
        , db
        )
from . import cypher as C
from typing import Union, Optional

@dataclass(frozen=True)
class RelationRepo:
    label:StructuredNode
    relation:str

    def find(self,
             uid:str,
             minmax_dist:Union[Optional[int],
                    tuple[Optional[int],Optional[int]]]
        )->Result:
        uniq = C.UniqIdNode(self.label, uid)
        rel = getattr(self.label, self.relation)
        p = C.Path(rel, minmax_dist, source=uniq.var)
        query = f"""
            MATCH {uniq.text}
            MATCH p = {p.text}
            RETURN nodes(p)
        """
        results, columns = db.cypher_query(query, resolve_objects=True)
        resolved = [r[0][0][p.result_index] for r in results]
        return Result(resolved, columns)

    def find_tips(self, uid:str):
        uniq = C.UniqIdNode(self.label, uid)
        rel = getattr(self.label, self.relation)
        p = C.Path(rel, None, source=uniq.var)
        tip_path = C.Path(rel, minmax_dist=1,
            source=p.matched, matched=None)
        query = f"""
            MATCH {uniq.text}
            MATCH {p.text}
            WHERE NOT {tip_path.text}
            RETURN {p.matched}
        """
        results, columns = db.cypher_query(query, resolve_objects=True)
        return Result([r[0] for r in results], columns)


@dataclass(frozen=True)
class Result:
    resolved:list[StructuredNode]
    params:dict[str]

    @property
    def uids(self)->set[str]:
        return set([r.uid for r in self.resolved])
    @property
    def names(self)->set[str]:
        return set([r.name for r in self.resolved])

    #         RETURN
    #             src
    #             , COUNT {(src)-[:INFER]->(tmp:Concept)} as cnt_dests
    #             , COUNT {(src)-[:INFER*2]->(tmp:Concept)} as cnt_dests_ord2
    #             , length(p) as distance
    #     """
    #     results, columns = db.cypher_query(query, params={"uid": uid}, resolve_objects=True)
    #     # return [Concept.inflate(r[0]) for r in results]
