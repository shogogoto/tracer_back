from .text import CypherText
from typing import Hashable, Union
from dataclasses import dataclass
from neomodel import StructuredNode


@dataclass(frozen=True)
class Node(CypherText):
    label:StructuredNode
    var:str = ""

    def build(self)->str:
        labs = ":".join(self.label.inherited_labels())
        return f"({self.var}:{labs})"

    def with_where(self, key, value, is_not:bool=False)->str:
        if isinstance(value, str):
            v = f"'{value}'"
        else:
            v = value
        not_ = "NOT " if is_not else ""
        return f"{self.text} WHERE {not_}{self.var}.{key} = {v}"


@dataclass(frozen=True)
class NoneNode(CypherText):
    def build(self)->str:
        return "()"

    @property
    def var_str(self)->str:
        return "()"
