from fastapi import HTTPException, status
from dataclasses import dataclass
from .param import Item
from pydantic.typing import Callable
from abc import ABC, abstractmethod


class DomainError(HTTPException):
    status_code:int
    title:str

    def __new__(cls, *args, **kwargs):
        dataclass(cls)
        return super().__new__(cls)

    @property
    def detail(self)->dict:
        return {
            "title": self.title
          , "message": self.message
        }

class AlreadyCreatedError(DomainError):
    item:Item
    status_code:int = status.HTTP_409_CONFLICT
    title:str = "Already created"

    @property
    def message(self)->str:
        return f"This is already exists: {self.item}"

class NotFoundError(DomainError):
    uid:str
    status_code:int = status.HTTP_404_NOT_FOUND
    title:str = "Not found"

    @property
    def message(self)->str:
        return f"This is not exists: uid={self.uid}"


class AlreadyConnectedError(DomainError):
    src_item:Item
    dest_item:Item
    status_code:int = status.HTTP_409_CONFLICT
    title:str = "Already connected"

    @property
    def message(self)->str:
        return "This is already connected" \
               f"from {self.src_item}" \
               f"to {self.dest_item}"

class NotConnectedError(DomainError):
    src_item:Item
    dest_item:Item
    status_code:int = status.HTTP_404_NOT_FOUND
    title:str = "Not connected"

    @property
    def message(self)->str:
        return "This is not connected" \
               f"from {self.src_item}" \
               f"to {self.dest_item}"
