from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base import CRUDBase
from app.domain.models.user import User
from app.core.security import get_password_hash
from app.domain.schemas.user_schema import UserCreate

class UserRepository(CRUDBase[User]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role.value if obj_in.role else None,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repo = UserRepository(User)
