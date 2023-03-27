from .node import ConceptNode
from ..param import Item
from ..repo import Concept


# 複数ノードを一括永続化するのに便利なツールを作りたい
#  永続化されていないデータが混在しててもOK
def test_concept_is_persisted():
    c = Concept(name="n")
    n1 = ConceptNode.of(c)
    assert not n1.is_persisted()

    n2 = ConceptNode.of(c.save())
    assert n2.is_persisted()

    n3 = ConceptNode.of(Item.create(name="xx"))
    assert not n3.is_persisted()

# 永続化済みか否かは同一性に影響しない
def test_node_eq():
    name = "test_eq"
    item = Item.create(name)
    n1 = ConceptNode.of(item)
    # n1 = ConceptNode.of("dummy")
    c  = Concept(name=name).save()
    n2 = ConceptNode.of(c)
    assert n1 == n2
