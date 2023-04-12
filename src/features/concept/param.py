from __future__ import annotations
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional


class Item(BaseModel):
    name: str
    description:Optional[str] = None
    uid:Optional[str] = None
    id:Optional[int] = None

    def exists(self)->bool:
        return self.id is not None
