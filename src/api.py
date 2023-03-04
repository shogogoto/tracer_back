from fastapi import FastAPI
from . import features as F


app = FastAPI()
app.include_router(F.concept.api.router)


@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
