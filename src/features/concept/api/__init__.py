from fastapi import APIRouter

from ..repo  import Concept
from . import parameter as P

router = APIRouter(
        prefix="/concepts",
        tags=["concept"]
        )

@router.get("")
async def invoke():
    all_nodes = Concept.nodes.all()
    return all_nodes




@router.put("")
async def invoke(item: P.Item):
    c = Concept(
            name=item.name,
            description=item.description
            ).save()
    return c
