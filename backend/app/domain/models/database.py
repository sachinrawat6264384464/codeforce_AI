import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.domain.models.base import Base

class ConnectedDatabase(Base):
    __tablename__ = "connected_databases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    db_type = Column(String, nullable=False)  # postgresql, mysql, etc.
    host = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    db_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    encrypted_password = Column(String, nullable=True)
    ssl_enabled = Column(Boolean, default=False)
    cloud_url = Column(String, nullable=True)  # For Snowflake/BigQuery
    status = Column(String, default="connected")
    last_sync_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User")
    sync_logs = relationship("SyncLog", back_populates="database", cascade="all, delete-orphan")


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    database_id = Column(UUID(as_uuid=True), ForeignKey("connected_databases.id"), nullable=False)
    status = Column(String, nullable=False)  # in_progress, success, failed
    message = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    database = relationship("ConnectedDatabase", back_populates="sync_logs")
