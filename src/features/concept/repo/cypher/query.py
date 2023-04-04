from typing import Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from neomodel import db

from .result import Result
from . import UniqIdNode
from .path import Path


class Query(ABC, Callable):
    @abstractmethod
    def __call__(self)->Result:
        pass


@dataclass
class FromUniqIdQuery(Query):
    uniq:UniqIdNode
    path:Path

    def __call__(self)->Result:
        query = f"""
            MATCH {self.uniq.text}
            MATCH p = {self.path.text}
            RETURN nodes(p)
        """
        results, columns = db.cypher_query(query, resolve_objects=True)
        resolved = [r[0][0][self.path.result_index] for r in results]
        return Result(resolved, columns)


@dataclass
class FromUniqIdToTipsQuery(Query):
    uniq:UniqIdNode
    path:Path

    def __post_init__(self):
        self.tip_path = Path(self.path.rel, minmax_dist=1,
            source=self.path.matched, matched=None)

    def __call__(self)->Result:
        query = f"""
            MATCH {self.uniq.text}
            MATCH {self.path.text}
            WHERE NOT {self.tip_path.text}
            RETURN {self.path.matched}
        """
        results, columns = db.cypher_query(query, resolve_objects=True)
        return Result([r[0] for r in results], columns)
