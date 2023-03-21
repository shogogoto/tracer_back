from .router import router
from ..repo import Concept
from ..param import Item


@router.post("/{uid}/sources")
async def create(uid: str, item: Item):
    c = Concept.nodes.first(uid=uid)
    src = item.toModel().save()
    src.dist.connect(c)
    print(src.__properties__)
    print(c.__properties__)
    return c

@router.get("/{uid}/sources")
async def find(uid: str):
    pass



@router.post("/{uid}/destinations")
def create(uid: str, item: Item):
    c = Concept.nodes.first(uid=uid)
    dist = item.toModel().save()
    c.dist.connect(dist)
    print(c)
    print(dist)
    return dist
