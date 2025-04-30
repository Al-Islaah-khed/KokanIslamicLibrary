from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status,Request

from repositories.user_repo import UserRepo
from helpers.password_hash import get_password_hash,verify_password
from models.user import User
from db.database import get_db
from helpers.token import verify_token,generate_token
import schemas.user as UserSchema
from datetime import timedelta

from config import Settings

settings = Settings()

# Authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = UserRepo.get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# Create User
def create_user(db: Session, user: UserSchema.UserCreate):
    existing_user = UserRepo.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user.password = get_password_hash(user.password)

    return UserRepo.create_user(db=db, user=user)


# Login user
def login_user(db:Session,user : UserSchema.UserLogin):
    found_user = authenticate_user(db,user.email,user.password)

    if not found_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email and password")

    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
            "fullname" : found_user.fullname,
            "email":found_user.email,
            "id": found_user.id,
            "is_admin": found_user.is_admin,
            "is_active":found_user.is_active,
        }

    if found_user.roles:
        data["roles"] = [role.name for role in found_user.roles]

    token = generate_token(data=data,expires_delta=token_expires)
    return UserSchema.UserLoginResponse(token=token,user=UserSchema.User(**data))


# Get current user from database
async def get_current_user(
    request : Request,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token),
):

    if hasattr(request.state, "user"):
        return request.state.user

    email = payload.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing email information"
        )

    user = UserRepo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    request.state.user = user
    return user

# Check if current user is active
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
