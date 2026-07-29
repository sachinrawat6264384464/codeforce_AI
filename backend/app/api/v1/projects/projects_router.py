from fastapi import APIRouter, Depends
from typing import List, Any
from app.api.dependencies import get_current_user
from app.domain.models.user import User

router = APIRouter()

@router.get("/")
def list_projects(current_user: User = Depends(get_current_user)) -> Any:
    return [{"id": "1", "name": "Sample Hospital Project", "status": "ACTIVE"}]

@router.post("/")
def create_project(name: str, current_user: User = Depends(get_current_user)) -> Any:
    return {"id": "2", "name": name, "status": "ACTIVE"}
