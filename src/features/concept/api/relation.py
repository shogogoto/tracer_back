from .router import router
from ..repo import Concept
from .param import Item
import json


@router.post("/{uid}/sources")
async def create(uid: str, item: Item):
    c = Concept.nodes.first(uid=uid)
    src = item.toModel().save()
    src.dist.connect(c)
    print(src.__properties__)
    print(c.__properties__)
    return c

@router.post("/{uid}/destinations")
def create(uid: str, item: Item):
    c = Concept.nodes.first(uid=uid)
    dist = item.toModel().save()
    c.dist.connect(dist)
    return dist
