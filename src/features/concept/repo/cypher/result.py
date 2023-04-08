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
class ResolvedResult:
    values:list[StructuredNode]

    @property
    def propkeys(self)->list[str]:
        if len(self.values) == 0:
            return []
        first = self.values[0]
        return list(first.__properties__.keys())


    # 複数形のprop attr name
    @property
    def plural_propkeys(self)->list[str]:
        return [k + "s" for k in self.propkeys]

    def __getattr__(self, name:str):
        plurals = self.plural_propkeys
        if name in plurals:
            i = plurals.index(name)
            key = self.propkeys[i]
            ls = [getattr(v, key) for v in self.values]
            return set(ls)
        else:
            return set()

    def __getitem__(self, n)->StructuredNode:
        return sel.values[n]



@dataclass(frozen=True)
class Results:
    results:list[list]
    columns:list[str]
    stats_columns:list[str]

    @property
    def resolved_columns(self)->list[str]:
        return [
            col for col in self.columns
                if col not in self.stats_columns
        ]

    def __getitem__(self, n:int):
        return self.results[n]

    def __getattr__(self, name)->set:
        if len(self.resolved_columns) == 1:
            r = [r[0] for r in self.results]
            resolved = ResolvedResult(r)
            return getattr(resolved, name)

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

