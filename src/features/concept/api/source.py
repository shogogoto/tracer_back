from ...common import routers
from ..param import Item, Parameter, Reconnection, ItemsView
from .. import usecase as UC
from fastapi import status

router = routers.create(
    "/concepts/{uid}/sources"
    , tags=["source"]
    )

@router.post(""
    , response_model=Item
    , status_code=status.HTTP_201_CREATED)
async def create_source(uid:str, param:Parameter):
    return UC.create_source(uid, param)

@router.post("/{src_uid}"
    , response_model=bool
    , status_code=status.HTTP_201_CREATED)
async def connect_to_source(uid:str, src_uid:str):
    return UC.connect(src_uid, uid)

@router.delete("/{src_uid}"
    , response_model=bool)
async def disconnect_to_source(uid:str, src_uid:str):
    return UC.disconnect(src_uid, uid)

@router.put("/{src_uid}"
    , response_model=bool)
async def replace_source(
    uid:str
    , src_uid:str
    , reconn:Reconnection
)->bool:
    return UC.change_infer_source(uid, src_uid, reconn.new_uid)

@router.get(""
    , response_model=Item)
async def find_sources(uid:str):
    return UC.find_sources(uid)
