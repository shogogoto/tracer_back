import pytest
from .usecase import UC
from .param import Item
from . import errors as E


def test_not_found():
    with pytest.raises(E.NotFoundError) as e:
        found = UC.find_by_uid(uid="dummy")

def test_create():
    item = Item(name="test", description="test")
    c = UC.create(item)
    assert c == UC.find_by_uid(c.uid)

def test_update():
    item = Item(name="for_update", description="test")
    with pytest.raises(E.NotFoundError) as e:
        UC.update(uid="dummy", item=item)
    c = UC.create(item)
    u = UC.update(uid=c.uid, item=Item(name="updated"))
    assert u == UC.find_by_uid(uid=c.uid)

def test_delete():
    item = Item(name="for_delete", description="test")
    assert not  UC.delete(uid="dummy")
    c = UC.create(item)
    UC.delete(uid=c.uid)
