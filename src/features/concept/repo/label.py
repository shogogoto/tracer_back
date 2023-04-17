from neomodel import (
    StructuredNode
    , UniqueIdProperty
    , StringProperty
    , RelationshipFrom
    , RelationshipTo
    , db
    , Relationship
    )


REL_TYPE: str = "INFER"

class Concept(StructuredNode):
    uid         = UniqueIdProperty()
    name        = StringProperty()
    description = StringProperty()
    # sourceは既に使われているプロパティ名っぽい
    srcs        = RelationshipFrom("Concept", REL_TYPE)
    dests       = RelationshipTo("Concept", REL_TYPE)
