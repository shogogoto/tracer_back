import networkx as nx
from ..param import Item
from typing import Optional, Union
from ..repo import Concept
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class ConceptNode:
    uid: Optional[str]
    name: str
    description: Optional[str]
    id: Optional[int] = None

    @classmethod
    def create(cls, data:Union[Item,Concept]):
        if isinstance(data, Item):
            return cls(uid=None, name=data.name, description=data.description)
        elif isinstance(data, Concept):
            return cls(
                uid=data.uid,
                name=data.name,
                description=data.description,
                id=getattr(data, "id", None)
                )
        else:
            raise TypeError()

    # DB上に存在するか
    def exists(self)->bool:
        return self.id is not None

    def json(self) -> dict:
        return {
            uid: self.uid,
            name: self.name,
            description: self.description
        }

    def model(self) -> Concept:
        pass

# 複数ノードを一括で作成するのに便利なツールを作りたい
class ConceptGraph:
    def __init__(self, data:Union[Item,Concept], uid:str=None):
        self._G = nx.DiGraph()
        self._uid = uuid4()
        self._G.add_node((self._uid, ConceptNode.create(data)))

    def add_sources(self, srcs:list[Union[Item,Concept]]):
        self._G.add_edges_from([((uuid4(), ConceptNode.create(s)), self._uid) for s in srcs])
        pass

    def add_distinations(self, dists:list[Union[Item,Concept]]):
        pass

    def sources(self, depth:int=1):
        # self._G.ed
        pass


    def save(self):
        pass

    @property
    def uid(self)->str:
        return str(self._uid)
