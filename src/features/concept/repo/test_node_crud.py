import pytest

from .node_crud import (
    ConceptCommand as Cmd
    , UidQuery
    )
from ..param import Item
from .. import errors as E


def test_create():
    item = Item(name="test_create")
    c = Cmd(item).create()
    assert c == UidQuery(c.uid).find()

def test_create_duplicate():
    item = Item(name="test_create_dup")
    created = Cmd(item).create()
    with pytest.raises(E.AlreadyCreatedError) as e:
        dup = Cmd(created).create()

def test_update():
    item = Item(name="test_pre_update")
    created = Cmd(item).create()
    up_item = Item(name="test_updated")
    u = Cmd(created).update(up_item)
    assert u == UidQuery(u.uid).find()

def test_update_not_found():
    item = Item(name="test_update_for_not_found")
    up_item = Item(name="test_updated_for_not_found")
    with pytest.raises(E.NotFoundError) as e:
        u = Cmd(item).update(up_item)

def test_delete():
    item = Item(name="test_delete")
    created = Cmd(item).create()
    assert Cmd(created).delete()

def test_delete_not_found():
    item = Item(name="test_delete_not_found")
    created = Cmd(item).create()
    assert Cmd(created).delete()
    with pytest.raises(E.NotFoundError) as e:
        Cmd(created).delete()
