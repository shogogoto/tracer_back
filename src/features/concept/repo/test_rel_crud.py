import pytest
from functools import cache
from .rel_crud import (
    ConnectionRepo as Cmd
    )
from .node_crud import ConceptCommand, WithStatisticsQuery
from ..param import Item
from .. import errors as E


def test_create():
    i1 = ConceptCommand(Item(name="test_conn1")).create()
    i2 = ConceptCommand(Item(name="test_conn2")).create()
    repo = Cmd(i1, i2)
    assert not repo.exists()
    assert repo.create()
    assert repo.exists()

def test_create_duplicate():
    i1 = ConceptCommand(Item(name="test_conn_dup_1")).create()
    i2 = ConceptCommand(Item(name="test_conn_dup_2")).create()
    repo = Cmd(i1, i2)
    repo.create()
    with pytest.raises(E.AlreadyConnectedError) as e:
        repo.create()

def test_replace():
    i1 = ConceptCommand(Item(name="test_replace_1")).create()
    i2 = ConceptCommand(Item(name="test_replace_2")).create()
    i3 = ConceptCommand(Item(name="test_replace_3")).create()
    repo1 = Cmd(i1, i2)
    repo2 = Cmd(i1, i3)
    with pytest.raises(E.NotConnectedError) as e:
        repo1.replace(i3)
    repo1.create()
    assert not repo2.exists()
    repo1.replace(i3)
    assert repo2.exists()

def test_delete():
    i1 = ConceptCommand(Item(name="test_delete_1")).create()
    i2 = ConceptCommand(Item(name="test_delete_2")).create()
    repo = Cmd(i1, i2)
    with pytest.raises(E.NotConnectedError) as e:
        repo.delete()
    repo.create()
    assert repo.delete()
    assert not repo.exists()
