from ..repo  import Concept
from .router import router
from . import param as P

import json
@router.get("")
async def find_all():
    all_nodes = Concept.nodes.all()
    # print(json.dumps(all_nodes), indent=2)
    for n in all_nodes:
        print(n)
        # print(dir(n))
        # print(n.__dict__)
        # print(n.__all_properties__)
        print(n.__properties__)
    return [n.__properties__ for n in all_nodes]

@router.post("")
async def create(item: P.Item):
    c = item.toModel().save()
    return c


@router.put("/{uid}")
async def update(uid: str, item: P.Item):
    c = Concept.nodes.first_or_none(uid=uid)
    c.save(
            name=item.name,
            description=item.description
           )
    return c


@router.delete("/{uid}")
async def delete(uid: str):
    c = Concept.nodes.first_or_none(uid=uid)
    return c.delete()
