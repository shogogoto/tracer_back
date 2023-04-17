from fastapi import APIRouter, FastAPI
from dataclasses import dataclass, field


@dataclass
class Routers:
    values:list[APIRouter] = field(default_factory=list)

    def create(self
        , prefix:str
        , tags:list[str] = None
    )->APIRouter:
        r = APIRouter(prefix=prefix, tags=tags)
        self.values.append(r)
        return r

    def batch_include(self, app:FastAPI)->None:
        for v in self.values:
            app.include_router(v)


routers = Routers()
