from __future__ import annotations
from dataclasses import dataclass, field
from textwrap import dedent
from .text import QueryBuilder, CypherText, Matcher
from .path import Path


class VarGenerator:
    __count:int = 0

    @classmethod
    def generate(cls)->str:
        var = f"gen_var_{cls.__count}"
        cls.__count += 1
        return var


@dataclass(frozen=True)
class Statistics:
    builder:QueryBuilder
    columns:list[str] = field(default_factory=list)

    def counted(self, path:Path, column:str)->Statistics:
        var = VarGenerator.generate()
        self.builder.add_text(Matcher(path, var=var, optional=True))
        c = Counter(var, column)
        self.builder.add_return(c.text)
        cols = self.columns + [column]
        return Statistics(self.builder, cols)

    def distanced(self, path:Path, column:str)->Statistics:
        var = VarGenerator.generate()
        self.builder.add_text(Matcher(path, var=var, optional=True))
        d = Distance(var, column)
        self.builder.add_return(d.text)
        cols = self.columns + [column]
        return Statistics(self.builder, cols)


@dataclass(frozen=True)
class Counter(CypherText):
    path_var:str
    column:str

    def build(self)->str:
        p = self.path_var
        return f"count(DISTINCT {p}) as {self.column}"


@dataclass(frozen=True)
class Distance(CypherText):
    path_var:str
    column:str

    def build(self)->str:
        p = self.path_var
        return f"avg(coalesce(length({p}), 0)) as {self.column}"
