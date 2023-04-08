from abc import ABC, abstractmethod
from typing import Hashable, Union, Callable
from dataclasses import dataclass, field
from neomodel import db
from .result import Result

class CypherText(ABC):
    @abstractmethod
    def build(self)->str:
        pass

    @property
    def text(self)->str:
        return self.build()

@dataclass(frozen=True)
class Where(CypherText):
    var:str
    key:str
    value:Union[str,int]
    with_not:bool = False

    def build(self)->str:
        if isinstance(self.value, str):
            v = f"'{self.value}'"
        else:
            v = self.value
        not_ = "NOT " if self.with_not else ""
        return f"WHERE {not_}{self.var}.{self.key}={v}"

@dataclass(frozen=True)
class Blank(CypherText):
    def build(self)->str:
        return ""


@dataclass(frozen=True)
class Matcher(CypherText):
    target:CypherText
    where:Where = Blank()
    var:str = None
    optional:bool = False

    def build(self)->str:
        t = self.target.text
        w = self.where.text
        if self.var is None:
            v = ""
        else:
            v = f"{self.var} = "
        o = "OPTIONAL " if self.optional else ""
        return f"{o}MATCH {v}{t} {w}"


@dataclass
class QueryBuilder(CypherText):
    matchers:list[Matcher] = field(default_factory=list)
    return_items:list[str] = field(default_factory=list)

    def add_text(self, t:CypherText)->CypherText:
        self.matchers.append(t)
        return t

    def add_return(self, item:str):
        self.return_items.append(item)

    def build(self)->str:
        matches = "\n".join([m.text for m in self.matchers])
        returns = "RETURN " + "\n, ".join(self.return_items)
        return matches + "\n" + returns

    def __call__(self)->Result:
        results, columns = db.cypher_query(
                self.text,
                resolve_objects=True)
        return Result([r[0] for r in results], columns)
