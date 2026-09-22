from typing import List
from fastapi import APIRouter
from app.dataaccess import database
from app.models.education import Education

router = APIRouter(prefix="/education",tags=["Education"])

@router.get("/",response_model=List[Education])
def get_education():
    return database.fetchall("SELECT eduId, education FROM education")


@router.get("/{eduId}",response_model=Education)
def get_education():
    return database.fetch_all("SELECT eduId, education FROM education")

@router.get("/{eduId}",response_model = Education)
def get_education_by_id(eduId:int):
    return database.fetch_one("SELECT eduId, education WHERE eduId = %s", (eduId, ))
