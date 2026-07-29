from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.dependencies import get_db, get_current_user
from app.domain.models.user import User
from app.domain.models.database import ConnectedDatabase
from app.domain.schemas.database import (
    DatabaseCreate, 
    DatabaseResponse, 
    DatabaseTest, 
    DatabaseMetadataResponse
)
from app.services.database.connection import test_connection
from app.services.database.encryption import encrypt_password
from app.services.database.metadata_discovery import get_metadata
from app.services.datahub.sync import sync_database_to_datahub

router = APIRouter()

@router.post("/test")
def test_db_connection(db_info: DatabaseTest):
    """Test connection without saving."""
    success, message = test_connection(db_info)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"status": "success", "message": message}

@router.post("/connect", response_model=DatabaseResponse)
def connect_database(
    db_info: DatabaseCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Save connection."""
    # First test it
    success, message = test_connection(DatabaseTest(**db_info.dict()))
    if not success:
        raise HTTPException(status_code=400, detail=message)
        
    db_obj = ConnectedDatabase(
        user_id=current_user.id,
        name=db_info.name,
        db_type=db_info.db_type,
        host=db_info.host,
        port=db_info.port,
        db_name=db_info.db_name,
        username=db_info.username,
        encrypted_password=encrypt_password(db_info.password) if db_info.password else None,
        ssl_enabled=db_info.ssl_enabled,
        cloud_url=db_info.cloud_url,
        status="connected"
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/list", response_model=List[DatabaseResponse])
def list_databases(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(ConnectedDatabase).filter(ConnectedDatabase.user_id == current_user.id).all()

@router.get("/{id}", response_model=DatabaseResponse)
def get_database(
    id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_obj = db.query(ConnectedDatabase).filter(ConnectedDatabase.id == id, ConnectedDatabase.user_id == current_user.id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Database not found")
    return db_obj

@router.delete("/{id}")
def delete_database(
    id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_obj = db.query(ConnectedDatabase).filter(ConnectedDatabase.id == id, ConnectedDatabase.user_id == current_user.id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Database not found")
    db.delete(db_obj)
    db.commit()
    return {"status": "success", "message": "Deleted"}

@router.post("/{id}/sync")
def trigger_sync(
    id: UUID, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_obj = db.query(ConnectedDatabase).filter(ConnectedDatabase.id == id, ConnectedDatabase.user_id == current_user.id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Database not found")
        
    background_tasks.add_task(sync_database_to_datahub, db_obj.id, db)
    return {"status": "sync_started", "message": "Metadata sync initiated"}

@router.get("/{id}/metadata")
def read_metadata(
    id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_obj = db.query(ConnectedDatabase).filter(ConnectedDatabase.id == id, ConnectedDatabase.user_id == current_user.id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Database not found")
        
    try:
        raw_meta = get_metadata(db_obj)
        return {
            "schemas": len(raw_meta.get("schemas", [])),
            "tables": len(raw_meta.get("tables", {})),
            "table_names": list(raw_meta.get("tables", {}).keys())[:4], # Send up to 4 tables for UI lineage
            "columns": sum(len(t.get("columns", [])) for t in raw_meta.get("tables", {}).values()),
            "relationships": raw_meta.get("relationships", 0),
            "views": len(raw_meta.get("views", {})),
            "owners": raw_meta.get("owners", 1),
            "lineage": raw_meta.get("lineage", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
