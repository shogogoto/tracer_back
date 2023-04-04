from typing import Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from neomodel import db

from .result import Result
from . import UniqIdNode
from .path import Path
from .statistics import Statistics



@dataclass
class Query(ABC, Callable):
    uniq:UniqIdNode
    path:Path

    def __call__(self, stats:Statistics = None)->Result:
        results, columns = db.cypher_query(self.text, resolve_objects=True)
        return self.resolve(results, columns)

    @property
    @abstractmethod
    def text(self)->str:
        pass

    @abstractmethod
    def resolve(self, results, columns)->Result:
        pass


@dataclass
class FromUniqIdQuery(Query):
    def resolve(self, results, columns)->Result:
        return Result(
            [r[0][0][self.path.result_index] for r in results]
            , columns)

    @property
    def text(self)->str:
        return f"""
            MATCH {self.uniq.text}
            MATCH p = {self.path.text}
            RETURN nodes(p)
        """


@dataclass
class FromUniqIdToTipsQuery(Query):
    def __post_init__(self):
        self.tip_path = Path(self.path.rel, minmax_dist=1,
            source=self.path.matched, matched=None)

    def resolve(self, results, columns):
        return Result([r[0] for r in results], columns)

    @property
    def text(self)->str:
        return f"""
            MATCH {self.uniq.text}
            MATCH {self.path.text}
            WHERE NOT {self.tip_path.text}
            RETURN {self.path.matched}
                //, COUNT
        """
