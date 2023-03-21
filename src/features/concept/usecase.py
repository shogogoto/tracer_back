from .repo import Concept
from .param import Item
from neomodel import db
from neomodel import exceptions
from . import errors as E

class UC:
    @classmethod
    def create(cls, item:Item) -> Concept:
        return cls._map(item).save()

    @classmethod
    def find_by_uid(cls, uid:str) -> Concept:
        try:
            return Concept.nodes.first(uid=uid)
        except exceptions.DoesNotExist as e:
            raise E.NotFoundError(str(e))

    @classmethod
    def update(cls, uid:str, item:Item) -> Concept:
        c = cls.find_by_uid(uid)
        c.name = item.name
        c.description = c.description
        return c.save()

    @classmethod
    def delete(cls, uid:str) -> bool:
        c = Concept.nodes.first_or_none(uid=uid)
        return c.delete() if c is not None else False

    @classmethod
    def _map(cls, item:Item):
        return Concept(name=item.name, description=item.description)

