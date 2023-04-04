from neomodel import RelationshipDefinition
from dataclasses import dataclass
from .text import CypherText
from enum import Enum, auto
from typing import Union, Optional
import types


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
class Path(CypherText):
    rel:RelationshipDefinition
    minmax_dist:MinMaxDistance
    source:str = "src"
    matched:str = "m"
    rel_var:str = ""

    def build(self)->str:
        ls = self.labels
        s = self.source_node
        m = self.matched_node
        arrow = self.arrow
        if self.direction == 1:
            return f"{s}{arrow}{m}"
        elif self.direction == -1:
            return f"{m}{arrow}{s}"
        else:
            raise ValueError("なんかdirectionは±1以外にもあるらしい")

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
    def arrow(self)->str:
        _type = self.rel.definition["relation_type"]
        distances = convert(self.minmax_dist)
        return f"-[{self.rel_var}:{_type}*{distances}]->"

    @property
    def tip_path(self)->str:
        pass

    @property
    def direction(self)->int:
        return self.rel.definition["direction"]

    @property
    def result_index(self)->int:
        if self.direction == 1:
            return -1
        else:
            return 0

