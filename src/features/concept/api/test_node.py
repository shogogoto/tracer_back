from pytest import fixture
from functools import cache
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from ..param import Parameter, Item
from .node import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

@fixture
@cache
def created_response():
    name  = "test_api_create"
    param = Parameter(name=name)
    return client.post("/concepts", json=param.dict())

def test_api_create_concept(created_response):
    name  = "test_api_create"
    res   = created_response
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["name"] == name

def test_api_update_concept():
    name = "test_api_update"
    param = Parameter(name=name)
    res = client.put("/concepts/not-found-uid", json=param.dict())
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json()["detail"]["title"] == "Not found"

    res = client.post("/concepts", json=param.dict())
    item = Item(**res.json())
    res = client.put(f"/concepts/{item.uid}", json=param.dict())
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["name"] == name

def test_api_delete_concept():
    name = "test_api_delete"
    param = Parameter(name=name)
    res = client.delete("/concepts/not-found-uid")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json()["detail"]["title"] == "Not found"

    res = client.post("/concepts", json=param.dict())
    item = Item(**res.json())
    res = client.delete(f"/concepts/{item.uid}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == True

def test_api_get_concept_by_uid(created_response):
    res = client.get("/concepts/not-found-uid")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() is None

    uid = created_response.json()["uid"]
    res = client.get(f"/concepts/{uid}")
    assert res.status_code == status.HTTP_200_OK
    assert created_response.json() == res.json()["item"]
