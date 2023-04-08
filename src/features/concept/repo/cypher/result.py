from dataclasses import dataclass, field
from neomodel import StructuredNode
from itertools import zip_longest


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

    def column(self, col_name):
        i = self.columns.index(col_name)
        return [r[i] for r in self.results]

    def __getattr__(self, name)->set:
        if len(self.resolved_columns) == 1:
            col_name = self.resolved_columns[0]
            col = self.column(col_name)
            resolved = ResolvedResult(col)
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

