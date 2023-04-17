from ...common import routers
from ..param import Item, Parameter
from .. import usecase as UC
from fastapi import status

router = routers.create("/concepts", ["concept"])

@router.post(""
    , response_model=Item
    , status_code=status.HTTP_201_CREATED)
async def create(param: Parameter):
    return UC.create_concept(param)

@router.put("/{uid}"
    , response_model=Item)
async def update(uid:str, param:Parameter):
    return UC.change_concept(uid, param)

@router.delete("/{uid}"
    , response_model=bool)
async def delete(uid: str):
    return UC.delete_concept(uid)
