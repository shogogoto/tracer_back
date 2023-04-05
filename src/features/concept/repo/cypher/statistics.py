from dataclasses import dataclass
from neomodel import RelationshipDefinition

from .path import Path


class Statistics:
    pass




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
        q = f"""
            p = {pstr}
            length(p) as {self.column}
        """
        return dedent(q).strip()
