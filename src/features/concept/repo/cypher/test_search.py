from .test_graph import narrow_tree, spread_tree
from .facade import PropQuery
from .. import Concept

def test_search_by_name(narrow_tree):
    g, _ = narrow_tree
    q = PropQuery(Concept)
    result = q.find("name", "test_source")
    return g.prop("name") == result.names
