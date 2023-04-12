from dataclasses import dataclass
from typing import Callable, Any

from .result import Results
from neomodel import StructuredNode

def to_prop(row:StructuredNode)->dict:
    return row.__properties__


@dataclass(frozen=True)
class DictConverter(Callable):
    value:Results
    resolved_convert:Callable = to_prop

    def __call__(self)->list[dict]:
        converter = self.__to_dict_func()
        return [
            converter(r)
            for r in self.value.results
        ]

    def __to_dict_func(self)->Callable:
        rsidx = self.value.resolved_index
        stidx = self.value.stats_index

        def func(row)->dict:
            d = {}
            for col, i in rsidx.items():
                d[col] = self.resolved_convert(row[i])
            for col, i in stidx.items():
                d[col] = row[i]
            return d
        return func
