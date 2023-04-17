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
    , TargetQuery
    )

from ..param import (
    StreamStatistics
    , Item
    , ItemView
    )
from .cypher import DictConverter


def stream_statistics(matched:Node)->Statistics:
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


class WithStatisticsQuery:
    @staticmethod
    def find_by_name(value:str)->Results:
        q = PropQuery(Concept)
        q.statistics = stream_statistics(q.matched)
        return q.find("name", value)

    @staticmethod
    def find_by_uid(uid:str)->Results:
        q = TargetQuery(Concept)
        q.statistics = stream_statistics(q.target)
        return q.find(uid)

    @staticmethod
    def find_adjacent_by_uid(uid:str)->tuple[Results,Results]:
        srcQ  = RelationQuery(Concept, "srcs")
        destQ = RelationQuery(Concept, "dests")
        srcQ.statistics  = stream_statistics(srcQ.matched)
        destQ.statistics = stream_statistics(destQ.matched)
        srcs  = srcQ.find(uid, 1)
        dests = destQ.find(uid, 1)
        return srcs, dests

    @staticmethod
    def find_sources(uid:str)->Results:
        srcQ  = RelationQuery(Concept, "srcs")
        srcQ.statistics  = stream_statistics(srcQ.matched)
        return srcQ.find(uid, 1)

    @staticmethod
    def find_destinations(uid:str)->Results:
        destQ = RelationQuery(Concept, "dests")
        destQ.statistics = stream_statistics(destQ.matched)
        return destQ.find(uid, 1)

    @staticmethod
    def find_stream_by_uid(uid:str)->tuple[Results,Results]:
        srcQ  = RelationQuery(Concept, "srcs")
        destQ = RelationQuery(Concept, "dests")
        srcQ.statistics  = stream_statistics(srcQ.matched)
        destQ.statistics = stream_statistics(destQ.matched)
        srcs  = srcQ.find(uid, None)
        dests = destQ.find(uid, None)
        return srcs, dests

    @staticmethod
    def results2model(res:Results)->list[ItemView]:
        dict_list = DictConverter(res)()
        def to_model(d:dict):
            item = Item(**d["matched"])
            s = StreamStatistics(
                upper_neighbor_count=d["src1"]
              , lower_neighbor_count=d["dest1"]
              , all_upper_count=d["src_all"]
              , all_lower_count=d["dest_all"]
              , max_distance_from_roots=d["root_distance"]
              , max_distance_from_leaves=d["leaf_distance"]
            )
            return ItemView(item=item, statistics=s)

        return [to_model(d) for d in dict_list]

