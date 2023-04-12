from dataclasses import dataclass
from . import Concept

from .cypher import (
    PropQuery
    , RelationQuery
    , Statistics
    , Results
    , Node
    , PathFactory
    , DictConverter
    )


def compas_statistics(matched:Node)->Statistics:
    n  = Node(Concept, "")
    f = PathFactory(Concept, matched)
    p1 = f("dests", 1,    n)
    p2 = f("dests", None, n)
    p3 = f("srcs", 1,     n)
    p4 = f("srcs", None,  n)
    tip1 = f.tip("dests")
    tip2 = f.tip("srcs")

    return Statistics() \
        .counted(p1, "dest1") \
        .counted(p2, "dest_all") \
        .counted(p3, "src1") \
        .counted(p4, "src_all") \
        .distanced(tip1, "leaf_distance", "max") \
        .distanced(tip2, "root_distance", "max")


@dataclass(frozen=True)
class WithStatisticsQuery:

    def find_by_name(self, value:str)->Results:
        q = PropQuery(Concept)
        q.statistics = compas_statistics(q.matched)
        return q.find("name", value)


    def find_adjacent_by_uid(self, uid:str)->tuple[Results,Results]:
        srcQ  = RelationQuery(Concept, "srcs")
        destQ = RelationQuery(Concept, "dests")
        srcQ.statistics  = compas_statistics(srcQ.matched)
        destQ.statistics = compas_statistics(destQ.matched)
        srcs  = srcQ.find(uid, 1)
        dests = destQ.find(uid, 1)
        return srcs, dests
