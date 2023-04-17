from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import features as F
from src.features.common import routers


app = FastAPI()

# COR許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.include_router(F.concept.api.concept_router)

app.include_router(F.admin.api.router)
routers.batch_include(app)


@app.get("/")
def read_root():
    return {"Hello": "World2"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
