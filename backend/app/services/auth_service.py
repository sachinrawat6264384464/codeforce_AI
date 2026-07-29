from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.core.security import verify_password, create_access_token
from app.domain.models.user import User

class AuthService:
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = user_repo.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_token_for_user(user: User) -> str:
        # subject can be the user id
        return create_access_token(subject=user.id)
