from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import CredentialsException
from app.database.session import SessionLocal
from app.domain.models.user import User
from app.repositories.user_repo import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db)
) -> User:
    # Hackathon Mock Auth: Always return a default admin user
    import uuid
    mock_user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    user = user_repo.get(db, id=mock_user_id)
    if not user:
        user = User(
            id=mock_user_id,
            email="superadmin@contextforge.ai",
            hashed_password="mock",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
