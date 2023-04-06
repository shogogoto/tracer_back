from __future__ import annotations
from dataclasses import dataclass, field
from textwrap import dedent

from .path import Path


@dataclass(frozen=True)
class StatisticsList:
    values:list[Statistics]

    def add(self, s:Statistics)->StatisticsList:
        return StatisticsList(self.values + [s])

    def x(self, result, res_columns)->dict[str,int]:
        columns = [v.column for v in self.values]
        col_idxs = [(c, res_columns.index(c)) for c in columns]
        return [
            {n: r[i] for n, i in col_idxs}
            for r in results
        ]

@dataclass(frozen=True)
class Statistics:
    pass
    # def add(self, other:Statistics)->StatisticsList:
    #     return StatisticsList(










@dataclass(frozen=True)
class Counter(Statistics):
    path:Path
    column:str

    @property
    def text(self)->str:
        pstr = self.path.build()
        return f"COUNT {{ {pstr} }} as {self.column}"


@dataclass(frozen=True)
class MaxDistance(Statistics):
    path:Path
    column:str

    @property
    def text(self)->str:
        pstr = self.path.build()
        return f"length({pstr}) as {self.column}"
