from ...common import routers
from ..param import (
    Item
    , Parameter
    , ItemView
    , ItemsView
    , StreamView
    )
from .. import usecase as UC
from fastapi import status
from typing import Optional

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


@router.get(""
    , response_model=ItemsView)
async def find_by_name_regex(name:str):
    return UC.find_by_name(name)

@router.get("/{uid}"
    , response_model=ItemView)
async def find_by_uid(uid:str):
    return UC.find_by_uid(uid)

@router.get("/{uid}/streams"
    , response_model=StreamView)
async def find_stream_by_uid(uid:str):
    return UC.find_stream_by_uid(uid)
