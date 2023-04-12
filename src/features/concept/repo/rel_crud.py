from __future__ import annotations
from . import Concept
from dataclasses import dataclass
from ..param import Item
from typing import Optional
from .. import errors as E
from .node_crud import UidQuery


@dataclass(frozen=True)
class ConnectionRepo:
    src:Item
    dest:Item

    def create(self)->bool:
        src, dest = self.mapper
        if src.dests.is_connected(dest):
            raise E.AlreadyConnectedError(self.src, self.dest)
        return src.dests.connect(dest)

    def replace(self, item:Item)->bool:
        self.delete()
        replaced = UidQuery(item.uid).find_strict()
        src, dest = self.mapper
        return src.dests.connect(replaced)

    def delete(self)->bool:
        src, dest = self.mapper
        if not src.dests.is_connected(dest):
            raise E.NotConnectedError(self.src, self.dest)
        src.dests.disconnect(dest)
        return True

    @property
    def mapper(self)->tuple[Concept,Concept]:
        return (
            UidQuery(self.src.uid).find_strict()
          , UidQuery(self.dest.uid).find_strict()
        )

    def exists(self)->bool:
        src, dest = self.mapper
        return src.dests.is_connected(dest)
