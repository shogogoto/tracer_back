from __future__ import annotations
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional


class Parameter(BaseModel):
    name:str
    description:Optional[str] = None


class Item(Parameter):
    uid:Optional[str] = None


class Connection(BaseModel):
    src_uid:str
    dest_uid:str


class SourceReconnection(Connection):
    new_src_uid:str


class DestinationReconnection(Connection):
    new_dest_uid:str


class StreamStatistics(BaseModel):
    upper_neighbor_count:int
    lower_neighbor_count:int
    all_upper_count:int
    all_lower_count:int
    max_distance_from_roots:int
    max_distance_from_leaves:int


class ItemView(BaseModel):
    item:Item
    statistics:StreamStatistics

class StreamView(BaseModel):
    sources:list[ItemView]
    destinations:list[ItemView]

