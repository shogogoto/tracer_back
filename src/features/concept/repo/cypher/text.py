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
