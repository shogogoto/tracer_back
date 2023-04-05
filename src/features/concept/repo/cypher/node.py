from .text import CypherText
from typing import Hashable
from dataclasses import dataclass
from neomodel import StructuredNode


@dataclass(frozen=True)
class Node(CypherText):
    label:StructuredNode
    var:str = "n"

    def build(self)->str:
        return self.var_str

    @property
    def var_str(self)->str:
        labs = ":".join(self.label.inherited_labels())
        return f"({self.var}:{labs})"


@dataclass(frozen=True)
class UniqIdNode(CypherText):
    label:StructuredNode
    uid:Hashable
    var:str = "target"

    def build(self)->str:
        labs = ":".join(self.label.inherited_labels())
        v    = self.var
        n = self.var_str
        return f"({v}:{labs}) WHERE {v}.uid = '{self.uid}'"

    @property
    def var_str(self)->str:
        labs = ":".join(self.label.inherited_labels())
        v    = self.var
        return f"({v}:{labs})"


@dataclass(frozen=True)
class NoneNode(CypherText):
    def build(self)->str:
        return "()"

    @property
    def var_str(self)->str:
        return "()"
