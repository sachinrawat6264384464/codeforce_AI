from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI, 
        pool_pre_ping=True,
        connect_args={"connect_timeout": 3}
    )
    with engine.connect() as conn:
        logger.info("Connected to PostgreSQL database successfully.")
except Exception as e:
    logger.warning(f"PostgreSQL connection failed ({e}). Falling back to local SQLite database.")
    sqlite_url = "sqlite:///./codeforge.db"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
