from .test_graph import narrow_tree
from . import result as R

def test_getattr_for_resolved_result(narrow_tree):
    g, _ = narrow_tree
    result = R.ResolvedResult(g.nodes)
    assert result.uids == set([r.uid for r in g.nodes])
    assert result.names == set([r.name for r in g.nodes])
    assert result.unknown_keys == set()

def test_getattr_empty():
    empty = R.ResolvedResult([])

    assert empty.uids == set()
    assert empty.unkwons == set()
