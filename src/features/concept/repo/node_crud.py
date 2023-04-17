from . import Concept
from dataclasses import dataclass
from ..param import Item
from typing import Optional
from .. import errors as E


def to_model(c:Concept):
    return Item(**c.__properties__)


@dataclass(frozen=True)
class ConceptCommand:
    item:Item

    def create(self)->Item:
        i = self.item
        if UidQuery(i.uid).exists():
            raise E.AlreadyCreatedError(item=i)
        c = Concept.create(i.dict())[0]
        return to_model(c)

    def update(self)->Item:
        c = UidQuery(self.item.uid).find_strict()
        for k, v in self.item.dict().items():
            if v is not None:
                setattr(c, k, v)
        s = c.save()
        return to_model(s)

    def delete(self)->bool:
        c = UidQuery(self.item.uid).find_strict()
        return c.delete()


@dataclass(frozen=True)
class UidQuery:
    uid:str

    def find(self)->Optional[Item]:
        c = Concept.nodes.first_or_none(uid=self.uid)
        if c is None:
            return None
        else:
            return to_model(c)

    def find_strict(self)->Concept:
        c = Concept.nodes.first_or_none(uid=self.uid)
        if c is None:
            raise E.NotFoundError(uid=self.uid)
        else:
            return c

    def exists(self)->bool:
        return self.find() is not None
