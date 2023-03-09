from fastapi import APIRouter

from ..repo  import Concept
from . import param as P

router = APIRouter(
        prefix="/concepts",
        tags=["concept"]
        )

@router.get("")
async def find_all():
    all_nodes = Concept.nodes.all()
    return all_nodes


@router.post("")
async def create(item: P.Item):
    c = Concept(
            name=item.name,
            description=item.description
            ).save()
    return c


@router.put("/{uid}")
async def update(uid: str, item: P.Item):
    c = Concept.nodes.first_or_none(uid=uid)
    print(c)
    c.save(
            name=item.name,
            description=item.description
           )
    return c


@router.delete("/{uid}")
async def delete(uid: str):
    c = Concept.nodes.first_or_none(uid=uid)
    return c.delete()
