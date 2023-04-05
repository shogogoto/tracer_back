from dataclasses import dataclass
from neomodel import RelationshipDefinition

from .path import Path


class Statistics:
    pass




@dataclass(frozen=True)
class Counter(Statistics):
    path:Path
    src:str = "src"
    dest:str = "dest"
    var:str = "count"

    @property
    def text(self):
        pstr = self.path.build()
        return f"COUNT {{ {pstr} }} as {self.var}"

    #         RETURN
    #             src
    #             , COUNT {(src)-[:INFER]->(tmp:Concept)} as cnt_dests
    #             , COUNT {(src)-[:INFER*2]->(tmp:Concept)} as cnt_dests_ord2
    #             , length(p) as distance
    #     """
    #     results, columns = db.cypher_query(query, params={"uid": uid}, resolve_objects=True)
    #     # return [Concept.inflate(r[0]) for r in results]
