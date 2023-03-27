from __future__ import annotations

from ..param import Item
from typing import Optional, Union
from ..repo import Concept
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class ConceptNode:
    value: Union[Item,Concept]
    uid: str = str(uuid4())

    @classmethod
    def of(cls, value:Union[Item,Concept]):
        if not isinstance(value, (Item,Concept)):
            raise TypeError(type(value))
        return cls(
                uid=getattr(value, "uid", str(uuid4())),
                value=value)

    @classmethod
    def batch_create(cls,
            name_descriptions:list[tuple(str,str)]
        )->list[ConcepNode]:
        return [
                cls.of(Concept(name=n, description=d))
                for n, d in name_descriptions
               ]


    def __eq__(self, other):
        sv = self.value
        ov = other.value
        return sv.name == ov.name \
            and sv.description == ov.description

    # 永続化済みか
    def is_persisted(self)->bool:
        return hasattr(self.value, "id") \
               and self.value.id is not None
