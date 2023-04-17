from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from ..param import Parameter, Item
from .node import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_api_create_concept():
    name  = "test_api_create"
    param = Parameter(name=name)
    res   = client.post("/concepts", json=param.dict())
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
