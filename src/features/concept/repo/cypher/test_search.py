from .test_graph import narrow_tree, spread_tree
from .facade import PropQuery
from .. import Concept


def test_search_by_name(narrow_tree):
    g, _ = narrow_tree
    q = PropQuery(Concept)
    result = q.find("name", "test_source")
    x = filter(lambda x: "test_source" in x, g.prop("name"))
    assert set(x) == result.names
