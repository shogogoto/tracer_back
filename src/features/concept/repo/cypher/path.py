from neomodel import RelationshipDefinition, StructuredNode
from dataclasses import dataclass, InitVar, field
from .text import CypherText
from .node import Node

from typing import Union, Optional


MinMaxDistance = Union[Optional[int],tuple[Optional[int],Optional[int]]]

def convert(value:MinMaxDistance)->str:
    if isinstance(value, int):
        return f"{value}"
    elif isinstance(value, tuple) \
            and len(value) in [1,2]:
        f = value[0] or ""
        if len(value) == 2:
            s = value[1] or ""
        else:
            s = ""
        return f"{f}..{s}"
    elif value is None:
        return ""
    types = list(map(type,value))
    raise TypeError(f"arg's type is invalid {types}")


@dataclass(frozen=True)
class PathArrow:
    rel:RelationshipDefinition
    minmax_dist:MinMaxDistance
    var:str = ""

    @property
    def labels(self)->str:
        return ":".join(
            self.rel.definition["node_class"]
            .inherited_labels())

    def node_str(var:Optional[str])->str:
        if var is None: return "()"
        return f"({var}:{self.labels})"

    @property
    def arrow(self)->str:
        _type = self.rel.definition["relation_type"]
        distances = convert(self.minmax_dist)
        return f"-[{self.var}:{_type}*{distances}]->"

    # OUTGOING, INCOMING, EITHER = 1, -1, 0
    def is_outgoing(self)->bool:
        return self.rel.definition["direction"] == 1


@dataclass
class Path(CypherText):
    arrow:PathArrow
    source:Node
    matched:Node

    def build(self)->str:
        s     = self.source.var_str
        m     = self.matched.var_str
        arrow = self.arrow.arrow
        if self.arrow.is_outgoing():
            return f"{s}{arrow}{m}"
        else:
            return f"{m}{arrow}{s}"

    @property
    def source_node(self)->str:
        return f"({self.source}:{self.labels})"

    @property
    def matched_node(self)->str:
        if self.matched is None: return "()"
        return f"({self.matched}:{self.labels})"

    @property
    def labels(self)->str:
        return ":".join(
            self.rel.definition["node_class"]
            .inherited_labels())

    @property
    def result_index(self)->int:
        if self.arrow.is_outgoing():
            return -1
        else:
            return 0


@dataclass(frozen=True)
class TipPath(CypherText):
    rel:RelationshipDefinition
    minmax_dist:MinMaxDistance
    source:str = "src"
    matched:str = "m"
    rel_var:str = ""

    pass
