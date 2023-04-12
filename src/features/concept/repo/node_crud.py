from . import Concept
from dataclasses import dataclass
from ..param import Item
from typing import Optional
from .. import errors as E
from .cypher.facade import PropQuery
from .cypher.result import Results
from .cypher.statistics import Statistics
from .cypher.node import Node
from .cypher.result_convert import DictConverter



@dataclass(frozen=True)
class ConceptCommand:
    item:Item

    def create(self)->Item:
        i = self.item
        if UidQuery(i.uid).exists():
            raise E.AlreadyCreatedError(item=i)
        c = Concept.create(i.dict())[0]
        return Item(**c.__properties__)

    def update(self, to:Item)->Item:
        c = UidQuery(self.item.uid).find_strict()
        for k, v in to.dict().items():
            if v is not None:
                setattr(c, k, v)
        s = c.save()
        return Item(**s.__properties__)

    def delete(self)->bool:
        c = UidQuery(self.item.uid).find_strict()
        return c.delete()


@dataclass(frozen=True)
class UidQuery:
    uid:str

    def find(self)->Optional[Item]:
        c = Concept.nodes.first_or_none(uid=self.uid)
        if c is None:
            return None
        else:
            return Item(**c.__properties__)

    def find_strict(self)->Concept:
        c = Concept.nodes.first_or_none(uid=self.uid)
        if c is None:
            raise E.NotFoundError(uid=self.uid)
        else:
            return c

    def exists(self)->bool:
        return self.find() is not None


@dataclass(frozen=True)
class WithStatisticsQuery:

    def find_by_name(self, value:str)->Results:
        q = PropQuery(Concept)
        n = Node(Concept, "")
        p1 = q.factory("srcs", 1, n)
        p2 = q.factory("dests", 1, n)
        p3 = q.factory.tip("srcs")
        p4 = q.factory.tip("dests")

        q.statistics = Statistics() \
                .counted(p1, "source1") \
                .counted(p2, "destination1") \
                .counted(p3, "roots") \
                .counted(p4, "leaves")
        return q.find("name", value)

    def find_adjacency_by_uid(self, uid:str):
        pass

