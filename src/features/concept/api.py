from fastapi import APIRouter

router = APIRouter()

@router.get("/concepts")
async def invoke():
    return {"x": "x"}
