from dataclasses import dataclass
from neomodel import (
        StructuredNode
        , StructuredRel
        , db
        )
from typing import Union, Optional, Callable, Hashable
from abc import ABC, abstractmethod
from . import Concept

# class CypherBuilder(ABC):
#     @abstractmethod
#     def build(self)->str:
#         pass

# @dataclass(frozen=True)
# class UniqIdMatcher(CypherBuilder):
#     label:StructuredNode
#     uid:Hashable
#     var:str = "n"

#     def build(self)->str:
#         labs = ":".join(self.label.inherited_labels())
#         return f"MATCH ({self.var}:{labs})" \
#                 f" WHERE {self.var}.uid = '{self.uid}''"

# @dataclass(frozen=True)
# class PathMatcher:
#     label:StructuredNode
#     source_var:str
#     min_dist:int = 1
#     max_dist:int = 1
#     var_name:str = "p"
#     pass


#     def cypher(self)->str:

#         srcs = getattr(Concept, "src2s")
#         print(srcs)
#         print(getattr(srcs, "definition"))
#         pass



# # 関係(edge)の統計情報
# @dataclass(frozen=True)
# class PathCounter:
#     pass


# @dataclass(frozen=True)
# class Query(Callable,CypherBuilder):
#     builders:list[CypherBuilder]


#     def __call__(self)->list[StructuredNode]:
#         q = self.build()
#         results, columns = db.cypher_query(
#                 q, resolve_objects=True)
#         print(results)

#         return self.build()

#     def build(self)->str:
#         print(self.builders[0])
#         q = " \n".join([b.build() for b in self.builders])
#         q += f"\n RETURN n"
#         return q

@dataclass(frozen=True)
class Result:
    resolved:list[StructuredNode]
    params:dict[str]

    @property
    def uids(self)->set[str]:
        return set([r.uid for r in self.resolved])
        # labels = [r[0][0][0] for r in self.results]
        # return set(elm.uid for elm in labels)

class RelationRepo:
    @classmethod
    def find_source(cls, uid:str, min_dist=1, max_dist=1):
        query = f"""
            MATCH (target:Concept) WHERE target.uid = $uid
            MATCH p = (src:Concept)-[rel:INFER*{min_dist}..{max_dist}]->(target)
        """ \
        """
            RETURN nodes(p) as sources
        """
        params = {"uid": uid}
        results, columns = db.cypher_query(
                query
                , params=params
                , resolve_objects=True)
        resolved = [r[0][0][0] for r in results]
        return Result(resolved, columns)


    @classmethod
    def find_dest(cls, uid:str, min_dist=1, max_dist=1):
        query = f"""
            MATCH (target:Concept) WHERE target.uid = $uid
            MATCH p = (target)-[rel:INFER*{min_dist}..{max_dist}]->(dest:Concept)
        """ \
        """
            RETURN nodes(p) as dests
        """
        params = {"uid": uid}
        results, columns = db.cypher_query(
                query
                , params=params
                , resolve_objects=True)
        for r in results:
            print(r)

        resolved = [r[0][0][-1] for r in results]
        return Result(resolved, columns)


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
