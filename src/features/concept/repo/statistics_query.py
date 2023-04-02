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


@dataclass(frozen=True)
class RelationRepo:
    label:StructuredNode
    relation:str

    @property
    def labels(self)->str:
        return ":".join(self.label.inherited_labels())

    @property
    def direction(self)->int:
        rel = getattr(self.label, self.relation)
        rel_def:dict = rel.definition
        return rel_def["direction"]

    @property
    def type(self)->str:
        rel = getattr(self.label, self.relation)
        rel_def:dict = rel.definition
        return rel_def["relation_type"]
    
    @property
    def result_index(self)->int:
        if self.direction == 1:
            return -1
        else:
            return 0

    def cypher_path(self, min_dist, max_dist)->str:
        direct_str = f"-[rel:{self.type}*{min_dist}..{max_dist}]->"
        if self.direction == 1:
            return f"p = (target){direct_str}(dest:{self.labels})"
        elif self.direction == -1:
            return f"p = (src:{self.labels}){direct_str}(target)"
        else:
            raise ValueError("なんかdirectionは±1以外にもあるらしい")


    def find(self, uid:str, min_dist=1, max_dist=1):
        p = self.cypher_path(min_dist, max_dist)
        query = f"""
            MATCH (target:{self.labels}) WHERE target.uid = $uid
            MATCH {p}
        """ \
        """
            RETURN nodes(p) as sources
        """
        # print(query)
        params = {"uid": uid}
        results, columns = db.cypher_query(
                query
                , params=params
                , resolve_objects=True)
        resolved = [r[0][0][self.result_index] for r in results]
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
