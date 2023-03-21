from fastapi.testclient import TestClient
from fastapi import FastAPI

from . import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_xxx():
    # res = client.delete("/concepts/dummyid")
    res = client.get("/concepts")
    # print(res)
    assert res.status_code == 200
    # print("####################")
    # print(res.json())
