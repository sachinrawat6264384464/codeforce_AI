from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.core.exceptions import BadRequestException
from app.domain.schemas.user_schema import UserCreate, UserResponse, Token
from app.domain.models.user import User
from app.repositories.user_repo import user_repo
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = AuthService.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise BadRequestException(detail="Incorrect email or password")
    elif not user.is_active:
        raise BadRequestException(detail="Inactive user")
        
    access_token = AuthService.create_token_for_user(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserResponse)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """Create new user without need to be logged in."""
    user = user_repo.get_by_email(db, email=user_in.email)
    if user:
        raise BadRequestException(
            detail="The user with this username already exists in the system."
        )
    user = user_repo.create_user(db, obj_in=user_in)
    return user

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get current user."""
    return current_user
