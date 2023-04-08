from __future__ import annotations
from dataclasses import dataclass, field
from textwrap import dedent
from .text import QueryBuilder, CypherText, Matcher, Callable
from .path import Path


class VarGenerator:
    __count:int = 0

    @classmethod
    def generate(cls)->str:
        var = f"gen_var_{cls.__count}"
        cls.__count += 1
        return var

CommandType = Callable[[QueryBuilder],None]

@dataclass(frozen=True)
class Statistics:
    columns:list[str] = field(default_factory=list)
    commands:list[CommandType] = field(default_factory=list)

    def counted(self, path:Path, column:str)->Statistics:
        def command(builder:QueryBuilder):
            var = VarGenerator.generate()
            builder.add_text(Matcher(path, var=var, optional=True))
            c = Counter(var, column)
            builder.add_return(c.text)
        return self.__add(column, command)

    def distanced(self, path:Path, column:str)->Statistics:
        def command(builder:QueryBuilder):
            var = VarGenerator.generate()
            builder.add_text(Matcher(path, var=var, optional=True))
            d = Distance(var, column)
            builder.add_return(d.text)
        return self.__add(column, command)

    def __add(self, column:str, command:Callable)->Statistics:
        cols = self.columns + [column]
        cmds = self.commands + [command]
        return Statistics(cols, cmds)

    def setup(self, builder:QueryBuilder):
        for c in self.commands:
            c(builder)


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
