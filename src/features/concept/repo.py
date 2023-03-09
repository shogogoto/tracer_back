from os import environ

from neomodel import (
        StructuredNode,
        UniqueIdProperty,
        StringProperty,
        )


class Concept(StructuredNode):
    uid         = UniqueIdProperty()
    name        = StringProperty()
    description = StringProperty()
