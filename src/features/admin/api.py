from fastapi import APIRouter
from neomodel import (
        db,
        install_all_labels,
        clear_neo4j_database
        )


router = APIRouter(
        prefix="/database",
        tags=["database"]
        )


@router.delete("")
async def clear():
    return clear_neo4j_database(db)

@router.post("")
async def install_labels():
    return install_all_labels()
