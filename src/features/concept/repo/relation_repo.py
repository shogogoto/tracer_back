from __future__ import annotations
from dataclasses import dataclass
from neomodel import (
        StructuredNode
        , db
        )
from . import cypher as C
from typing import Union, Optional, Callable


@dataclass(frozen=True)
class RelationRepo:
    label:StructuredNode
    relation:str
    resolved:bool = True

    def find(self,
             uid:str,
             minmax_dist:Union[Optional[int],
                    tuple[Optional[int],Optional[int]]]
        )->C.Result:
        uniq = C.UniqIdNode(self.label, uid)
        rel = getattr(self.label, self.relation)
        p = C.Path(rel, minmax_dist, source=uniq.var)
        query = f"""
            MATCH {uniq.text}
            MATCH p = {p.text}
            RETURN nodes(p)
        """
        print(query)
        results, columns = db.cypher_query(query, resolve_objects=True)
        resolved = [r[0][0][p.result_index] for r in results]
        return C.Result(resolved, columns)

    def find_tips(self, uid:str)->C.Result:
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
        print(query)
        results, columns = db.cypher_query(query, resolve_objects=True)
        return C.Result([r[0] for r in results], columns)

