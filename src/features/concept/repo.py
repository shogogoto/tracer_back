from __future__ import annotations
from os import environ

from neomodel import (
        StructuredNode,
        UniqueIdProperty,
        StringProperty,
        RelationshipFrom,
        RelationshipTo
        )


REL_TYPE: str = "INFER"

class Concept(StructuredNode):
    uid         = UniqueIdProperty()
    name        = StringProperty()
    description = StringProperty()
    dist        = RelationshipTo("Concept", REL_TYPE) # sourceは既に使われているプロパティ名っぽい
    # distination = RelationshipTo(cls, REL_TYPE)
