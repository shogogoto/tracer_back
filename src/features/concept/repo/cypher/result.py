from dataclasses import dataclass
from neomodel import StructuredNode


@dataclass(frozen=True)
class Result:
    resolved:list[StructuredNode]
    params:dict[str]

    @property
    def uids(self)->set[str]:
        return set([r.uid for r in self.resolved])
    @property
    def names(self)->set[str]:
        return set([r.name for r in self.resolved])
