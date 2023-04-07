from dataclasses import dataclass, field
from neomodel import StructuredNode
from itertools import zip_longest

@dataclass(frozen=True)
class Result:
    resolved:list[StructuredNode]
    params:dict[str]
    statistics_info:list[dict[str,int]] = field(default=list)

    @property
    def uids(self)->set[str]:
        return set([r.uid for r in self.resolved])
    @property
    def names(self)->set[str]:
        return set([r.name for r in self.resolved])

    def filter_(self, **kwargs):
        def condition(pair):
            r, _ = pair
            return all([
                getattr(r, k) == v
                for k,v in kwargs.items()
            ])
        return list(filter(condition, self.zip_()))

    def zip_(self):
        return zip_longest(self.resolved, self.statistics_info)

    def to_json(self):
        return [
            {
                "props": r.__properties__
              , "satistisc": s
            }
            for r, s in self.zip_()
        ]

    # def __getattribute__(self, name)->set[str]:
    #     return set([getattr(r, name) for r in self.resolved])

@dataclass(frozen=True)
class Results:
    results:list
    columns:list[str]
    stats_columns:list[str]

    def column(self, name)->list:
        i = self.columns.index(name)
        return [r[i] for r in self.results]

    def column_attrs(self, colname:str, attrname:str):
        col = self.column(colname)
        return [getattr(c, attrname) for c in col]

    def statistics(self)->list[dict]:
        i_stats = [
            self.columns.index(s)
            for s in self.stats_columns
        ]
        return [
            {
                self.columns[i]: r[i]
                for i in i_stats
             }
            for r in self.results
        ]

