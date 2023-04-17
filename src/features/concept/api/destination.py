from ..param import Item, Parameter, Reconnection
from .. import usecase as UC
from fastapi import status
from ...common import routers
# responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,

router = routers.create(
    prefix="/concepts/{uid}/destinations"
    , tags=["destination"]
    )

@router.post(""
    , response_model=Item
    , status_code=status.HTTP_201_CREATED)
async def create_destination(uid:str, param:Parameter):
    return UC.create_destination(uid, param)

@router.post("/{dest_uid}"
    , response_model=bool
    , status_code=status.HTTP_201_CREATED)
async def connect_to_destination(uid:str, dest_uid:str):
    return UC.connect(uid, dest_uid)

@router.delete("/{dest_uid}"
    , response_model=bool)
async def disconnect_to_destination(uid:str, dest_uid:str):
    return UC.disconnect(uid, dest_uid)

@router.put("/{dest_uid}"
    , response_model=bool)
async def replace_source(
    uid:str
    , dest_uid:str
    , reconn:Reconnection
)->bool:
    return UC.change_infer_destination(uid, dest_uid, reconn.new_uid)
