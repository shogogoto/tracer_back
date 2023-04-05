from typing import Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from neomodel import db
from textwrap import dedent

from .result import Result
from . import UniqIdNode
from .path import Path, PathArrow
from .node import Node, NoneNode
from .statistics import Statistics


@dataclass
class Statistics:
    pass



def compose_stats(results, columns, statistics):
    col_idxs = [(s.var, columns.index(s.var)) for s in statistics]
    return [
        {n: r[i] for n, i in col_idxs}
        for r in results
    ]

@dataclass
class Query(ABC, Callable):
    uniq:UniqIdNode
    path:Path

    def __call__(self, *stats:Statistics)->Result:
        txt = dedent(self.text)
        txt = "\n ,".join([txt] + [s.text for s in stats])
        txt = txt.strip()
        results, columns = \
            db.cypher_query(txt, resolve_objects=True)
        stats_info = compose_stats(results, columns, stats)
        return Result(self.to_neomodel(results), columns, stats_info)

    @property
    @abstractmethod
    def text(self)->str:
        pass

    @abstractmethod
    def to_neomodel(self, results):
        pass


@dataclass
class FromUniqIdQuery(Query):
    def to_neomodel(self, results):
        return [r[0][0][self.path.result_index] for r in results]

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
        arrow = PathArrow(self.path.arrow.rel, 1)
        self.tip_path = Path(arrow,
            source=self.path.matched,
            matched=NoneNode())

    def to_neomodel(self, results):
        return [r[0] for r in results]

    @property
    def text(self)->str:
        return f"""
            MATCH {self.uniq.text}
            MATCH {self.path.text} WHERE NOT {self.tip_path.text}
            RETURN {self.path.matched.var}
        """
