from .repo import (
    ConceptCommand
    , InferRepo
    , WithStatisticsQuery
    )
from .param import (
    Item
    , Parameter
    , ItemView
    , StreamView
    )
from neomodel import db


@db.write_transaction
def create_concept(param:Parameter)->Item:
    item = Item(**param.dict())
    return ConceptCommand(item).create()


@db.write_transaction
def create_source(uid:str, param:Parameter)->Item:
    src = Item(**param.dict())
    s = ConceptCommand(src).create()
    InferRepo(s.uid, uid).create()
    return s


@db.write_transaction
def create_destination(uid:str, param:Parameter)->bool:
    dest = Item(**param.dict())
    d = ConceptCommand(dest).create()
    InferRepo(uid, d.uid).create()
    return d


@db.write_transaction
def change_concept(uid:str, param:Parameter)->Item:
    item = Item(uid=uid, **param.dict())
    return ConceptCommand(item).update()

@db.write_transaction
def delete_concept(uid:str)->bool:
    item = Item(uid=uid, name="dummy")
    return ConceptCommand(item).delete()

@db.write_transaction
def connect(src_uid, dest_uid)->bool:
    return InferRepo(src_uid, dest_uid).create()


@db.write_transaction
def disconnect(src_uid:str, dest_uid:str)->bool:
    return InferRepo(src_uid, dest_uid).delete()


@db.write_transaction
def change_infer_source(
        dest_uid:str
        , src_old_uid:str
        , src_new_uid:str
    )->bool:
    return InferRepo(src_old_uid, dest_uid) \
            .replace_src(src_new_uid)


@db.write_transaction
def change_infer_destination(
        src_uid:str
        , dest_old_uid:str
        , dest_new_uid:str
    )->bool:
    return InferRepo(src_uid, dest_old_uid) \
            .replace_dest(dest_new_uid)


@db.read_transaction
def find_by_name(name:str)->list[ItemView]:
    results = WithStatisticsQuery.find_by_name(name)
    return WithStatisticsQuery.results2model(results)


@db.read_transaction
def find_stream_by_uid(uid:str)->StreamView:
    srcs, dests = WithStatisticsQuery().find_adjacent_by_uid(uid)
    return StreamView(
        sources=WithStatisticsQuery.results2model(srcs)
        , destinations=WithStatisticsQuery.results2model(dests)
    )
