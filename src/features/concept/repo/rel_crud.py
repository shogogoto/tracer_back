from __future__ import annotations
from . import Concept
from pydantic.dataclasses import dataclass
from ..param import Item
from typing import Optional
from .. import errors as E
from .node_crud import UidQuery


@dataclass(frozen=True)
class InferRepo:
    src_uid:str
    dest_uid:str

    def create(self)->bool:
        src, dest = self.mapper
        if src.dests.is_connected(dest):
            src_item = Item(**src.__properties__)
            dest_item = Item(**dest.__properties__)
            raise E.AlreadyConnectedError(src_item, dest_item)
        return src.dests.connect(dest)

    def replace_dest(self, dest_uid:str)->bool:
        self.delete()
        replaced = UidQuery(dest_uid).find_strict()
        src, dest = self.mapper
        return src.dests.connect(replaced)

    def replace_src(self, src_uid:str)->bool:
        self.delete()
        replaced = UidQuery(src_uid).find_strict()
        src, dest = self.mapper
        return dest.srcss.connect(replaced)

    def delete(self)->bool:
        src, dest = self.mapper
        if not src.dests.is_connected(dest):
            src_item = Item(**src.__properties__)
            dest_item = Item(**dest.__properties__)
            raise E.NotConnectedError(src_item, dest_item)
        src.dests.disconnect(dest)
        return True

    @property
    def mapper(self)->tuple[Concept,Concept]:
        return (
            UidQuery(self.src_uid).find_strict()
          , UidQuery(self.dest_uid).find_strict()
        )

    def exists(self)->bool:
        src, dest = self.mapper
        return src.dests.is_connected(dest)
