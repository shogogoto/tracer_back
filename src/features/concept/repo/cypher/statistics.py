from dataclasses import dataclass
from neomodel import RelationshipDefinition

from .path import Path


class Statistics:
    pass




@dataclass(frozen=True)
class Counter(Statistics):
    path:Path
    src:str = "src"
    dest:str = "dest"
    var:str = "count"

    @property
    def text(self):
        pstr = self.path.build()
        return f"COUNT {{ {pstr} WHERE true }} as {self.var}"
