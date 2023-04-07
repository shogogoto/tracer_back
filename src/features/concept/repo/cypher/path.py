from __future__ import annotations
from neomodel import StructuredNode, RelationshipDefinition
from dataclasses import dataclass
from .text import CypherText
from .node import Node, NoneNode

from typing import Union, Optional, Callable


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
class PathFactory(Callable):
    label:StructuredNode
    source:Node

    def __call__(self,
        relation:str
        , minmax_dist:MinMaxDistance
        , matched:Node
            )->Path:
        rel_def = self.rel_def(relation)
        return PathArrow(rel_def, minmax_dist) \
                .to_path(self.source, matched)

    def rel_def(self, relation:str)->RelationshipDefinition:
        return getattr(self.label, relation)


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

    def to_path(self, source:Node, matched:Node)->Path:
        return Path(self, source, matched)
        pass

@dataclass
class Path(CypherText):
    arrow:PathArrow
    source:Node
    matched:Node

    def build(self)->str:
        s     = self.source.text
        m     = self.matched.text
        arrow = self.arrow.text
        if self.arrow.is_outgoing():
            return f"{s}{arrow}{m}"
        else:
            return f"{m}{arrow}{s}"

    def tip(self)->TipPath:
        return TipPath(self)


@dataclass(frozen=True)
class TipPath(CypherText):
    source_path:Path

    def build(self)->str:
        sp    = self.source_path
        arrow = PathArrow(sp.arrow.rel, 1)
        n     = Node(self.source_path.matched.label, "")
        p     = Path(arrow, sp.matched, n)
        return f"{sp.text} WHERE NOT {p.text}"
