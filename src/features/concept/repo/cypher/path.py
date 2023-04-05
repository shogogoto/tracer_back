from __future__ import annotations
from neomodel import RelationshipDefinition
from dataclasses import dataclass
from .text import CypherText
from .node import Node, NoneNode

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
class PathArrow(CypherText):
    rel:RelationshipDefinition
    minmax_dist:MinMaxDistance
    var:str = ""

    def build(self)->str:
        _type = self.rel.definition["relation_type"]
        distances = convert(self.minmax_dist)
        return f"-[{self.var}:{_type}*{distances}]->"

    @property
    def labels(self)->str:
        return ":".join(
            self.rel.definition["node_class"]
            .inherited_labels())

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
        arrow = self.arrow.text
        if self.arrow.is_outgoing():
            return f"{s}{arrow}{m}"
        else:
            return f"{m}{arrow}{s}"

    @property
    def result_index(self)->int:
        if self.arrow.is_outgoing():
            return -1
        else:
            return 0

    def tip(self)->TipPath:
        return TipPath(self)


@dataclass(frozen=True)
class TipPath(CypherText):
    source_path:Path

    def build(self)->str:
        sp    = self.source_path
        arrow = PathArrow(sp.arrow.rel, 1)
        n     = NoneNode()
        p     = Path(arrow, sp.matched, n)
        return f"{sp.text} WHERE NOT {p.text}"
