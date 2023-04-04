from __future__ import annotations
from dataclasses import dataclass
from neomodel import (
        StructuredNode
        , db
        , RelationshipDefinition
        )
from . import cypher as C
from .cypher import query as Q
from typing import Union, Optional, Callable



Found = Union[C.Result, Q.Query]

@dataclass(frozen=True)
class RelationRepo:
    label:StructuredNode
    relation:str
    resolved:bool = True

    def find(self, uid:str, minmax_dist:C.path.MinMaxDistance)->Found:
        uniq = C.UniqIdNode(self.label, uid)
        p    = C.Path(self.rel_def, minmax_dist, source=uniq.var)
        q    = C.query.FromUniqIdQuery(uniq, p)
        return self.__resolove_and_return(q)

    def find_tips(self, uid:str)->Found:
        uniq     = C.UniqIdNode(self.label, uid)
        p        = C.Path(self.rel_def, None, source=uniq.var)
        q = C.query.FromUniqIdToTipsQuery(uniq, p)
        return self.__resolove_and_return(q)

    def __resolove_and_return(self, q:C.query.Query)->C.Result:
        if self.resolved:
            return q()
        else:
            return q

    @property
    def rel_def(self)->RelationshipDefinition:
        return getattr(self.label, self.relation)
