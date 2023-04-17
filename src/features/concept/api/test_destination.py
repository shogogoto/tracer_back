from pytest import fixture
from functools import cache
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from ..param import Parameter, Reconnection
from .destination import router

from ..repo.cypher.graph import NeoDiGraph
from ..repo import Concept
from ..usecase import find_stream_by_uid


app = FastAPI()
app.include_router(router)
client = TestClient(app)

@fixture
@cache
def g():
    g = NeoDiGraph(Concept)
    for i in range(8):
        g.add_node(name=f"test_api_dest{i}")
    return g


def test_api_create_dest(g):
    uid1 = g.nodes[0].uid
    param = Parameter(name="create_dest")
    res   = client.post(f"/concepts/{uid1}/destinations", json=param.dict())
    assert res.status_code == status.HTTP_201_CREATED
    sv = find_stream_by_uid(uid1)
    assert res.json()["uid"] == sv.destinations[0].item.uid

def test_api_connect_to(g):
    uid2 = g.nodes[1].uid
    uid3 = g.nodes[2].uid
    res   = client.post(f"/concepts/{uid2}/destinations/{uid3}")
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json() == True
    sv = find_stream_by_uid(uid2)
    assert uid3 == sv.destinations[0].item.uid

def test_api_disconnect_to(g):
    uid4 = g.nodes[3].uid
    uid5 = g.nodes[4].uid
    g.add_edge(uid4, uid5)
    res   = client.delete(f"/concepts/{uid4}/destinations/{uid5}")
    assert res.status_code == status.HTTP_200_OK
    sv = find_stream_by_uid(uid4)
    assert len(sv.destinations) == 0

def test_api_replace_dest(g):
    uid6 = g.nodes[5].uid
    uid7 = g.nodes[6].uid
    uid8 = g.nodes[7].uid
    g.add_edge(uid6, uid7)
    reconn = Reconnection(new_uid=uid8)
    res   = client.put(f"/concepts/{uid6}/destinations/{uid7}"
            , json=reconn.dict())
    assert res.status_code == status.HTTP_200_OK
    sv = find_stream_by_uid(uid6)
    assert uid8 == sv.destinations[0].item.uid
