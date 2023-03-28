from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from neomodel import StructuredNode
from .repo import Concept


class Item(BaseModel):
    name: str
    description: Optional[str] = None

    def toModel(self) -> StructuredNode:
        return Concept(
                name=self.name,
                description=self.description
                )

    @classmethod
    def create(cls,
            name:str,
            description:str = None
        )->Item:
        return cls(name=name, description=description)
