from abc import ABC, abstractmethod
from typing import Hashable
from dataclasses import dataclass
from neomodel import StructuredNode, RelationshipDefinition

class CypherText(ABC):
    @abstractmethod
    def build(self)->str:
        pass

    @property
    def text(self)->str:
        return self.build()


@dataclass(frozen=True)
class UniqIdNode(CypherText):
    label:StructuredNode
    uid:Hashable
    var:str = "target"

    def build(self)->str:
        labs = ":".join(self.label.inherited_labels())
        v    = self.var
        n = self.node_str
        return f"({v}:{labs}) WHERE {v}.uid = '{self.uid}'"

    @property
    def node_str(self)->str:
        labs = ":".join(self.label.inherited_labels())
        v    = self.var
        return f"({v}:{labs})"
