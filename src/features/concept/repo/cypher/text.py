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
class Matcher(CypherText):
    operand:str
    var:str = None

    def build(self)->str:
        if self.var is None:
            v = ""
        else:
            v = f"{self.var} = "
        return f"MATCH {v}{self.operand}"

@dataclass
class QueryResolver(CypherText, Callable):
    matchers:list[Matcher] = field(default_factory=list)
    return_items:list[str] = field(default_factory=list)

    def add_matcher(self, operand:str, var:str=None)->Matcher:
        m = Matcher(operand, var)
        self.matchers.append(m)
        return m

    def add_return(self, item:str):
        self.return_items.append(item)

    def build(self)->str:
        matches = "\n".join([m.text for m in self.matchers])
        returns = "RETURN " + ", ".join(self.return_items)
        return matches + "\n" + returns

    def __call__(self)->Result:
        results, columns = db.cypher_query(
                self.text,
                resolve_objects=True)
        return Result([r[0] for r in results], columns)
