from __future__ import annotations
from dataclasses import dataclass
from neomodel import (
        StructuredNode
        , db
        , RelationshipDefinition
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
             minmax_dist:Union[Optional[int],tuple[Optional[int],Optional[int]]]
        )->C.Result:
        uniq = C.UniqIdNode(self.label, uid)
        p    = C.Path(self.rel_def, minmax_dist, source=uniq.var)
        q    = C.query.FromUniqIdQuery(uniq, p)
        return self.__resolove_and_return(q)

    def find_tips(self, uid:str)->C.Result:
        uniq     = C.UniqIdNode(self.label, uid)
        p        = C.Path(self.rel_def, None, source=uniq.var)
        q = C.query.FromUniqIdToTipsQuery(uniq, p)
        return self.__resolove_and_return(q)

    def __resolove_and_return(self, q:C.query.Query)->C.Result:
        return q() if self.resolved else q

    @property
    def rel_def(self)->RelationshipDefinition:
        return getattr(self.label, self.relation)
