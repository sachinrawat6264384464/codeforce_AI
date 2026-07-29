from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class DatabaseBase(BaseModel):
    name: str = Field(..., description="A friendly name for the connection")
    db_type: str = Field(..., description="Database type (e.g. postgresql, mysql)")
    host: Optional[str] = None
    port: Optional[int] = None
    db_name: Optional[str] = None
    username: Optional[str] = None
    ssl_enabled: bool = False
    cloud_url: Optional[str] = None

class DatabaseCreate(DatabaseBase):
    password: Optional[str] = None

class DatabaseTest(DatabaseBase):
    password: Optional[str] = None

class DatabaseResponse(DatabaseBase):
    id: UUID
    user_id: UUID
    status: str
    last_sync_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SyncLogResponse(BaseModel):
    id: UUID
    database_id: UUID
    status: str
    message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class DatabaseMetadataResponse(BaseModel):
    schemas: int = 0
    tables: int = 0
    columns: int = 0
    relationships: int = 0
    views: int = 0
    owners: int = 0
    lineage: int = 0
    
class SyncStatusResponse(BaseModel):
    status: str
    progress: int
    message: str
