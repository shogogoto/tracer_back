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


def to_model(c:Concept)->Item:
    return Item(**c.__properties__)

def to_mapper(item:Item)->Concept:
    return Concept(**item.dict())


# エラー
@dataclass(frozen=True)
class CommandRepo:
    item:Item

    def create(self)->Item:
        i = self.item
        if i.exists():
            raise E.AlreadyCreatedError(item=i)
        c = Concept.create(i.dict())[0]
        return to_model(c)

    def update(self, to:Item)->Item:
        c = UidQuery(self.item.uid).find_strict()
        c = to_mapper(c)
        for k, v in to.dict().items():
            if v is not None:
                setattr(c, k, v)
        s = c.save()
        return to_model(s)

    def delete(self)->bool:
        c = UidQuery(self.item.uid).find_strict()
        return Concept(**c.dict()).delete()

    def connect_dest(self, dest_item:Item):
        if not self.item.exists():
            raise E.NotFoundError(src_item)
        if not dest_item.exists():
            raise E.NotFoundError(src_item)
        src  = to_mapper(self.item)
        src.refresh()
        dest = to_mapper(dest_item)
        dest.refresh()
        src.dests.connect(dest)

    def connect_src(self, src_item:Item):
        if not src_item.exists():
            raise E.NotFoundError(src_item)
        if not self.item.exists():
            raise E.NotFoundError(src_item)
        src  = to_mapper(src_item)
        src.refresh()
        dest = to_mapper(self.item)
        dest.refresh()
        src.dests.connect(dest)


@dataclass(frozen=True)
class UidQuery:
    uid:str

    def find(self)->Optional[Item]:
        c = Concept.nodes.first_or_none(uid=self.uid)
        if c is None:
            return N
        else:
            return Item(**c.__properties__)

    def find_strict(self)->Item:
        c = Concept.nodes.first_or_none(uid=self.uid)
        if c is None:
            raise E.NotFoundError(uid=self.uid)
        else:
            return Item(**c.__properties__)


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
