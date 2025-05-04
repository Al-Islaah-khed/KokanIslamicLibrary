from sqlalchemy.orm import Session
from fastapi import  HTTPException, status

from repositories.user_repo import UserRepo
from helpers.password_hash import get_password_hash,verify_password
from helpers.token import generate_token
import schemas.user as UserSchema
from datetime import timedelta
from helpers.logger import logger

from config import Settings

settings = Settings()

# Authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = UserRepo.get_user_by_email(db=db, email=email)
    if not user:
        logger.warning(f"Authentication failed: user with email '{email}' not found")
        return None
    if not verify_password(password, user.password):
        logger.warning(f"Authentication failed: incorrect password for user '{email}'")
        return None
    logger.info(f"User '{email}' authenticated successfully")
    return user

# Create User
def create_user(db: Session, user: UserSchema.UserCreate):
    existing_user = UserRepo.get_user_by_email(db, user.email)
    if existing_user:
        logger.warning(f"User creation failed: email '{user.email}' already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user.password = get_password_hash(user.password)
    created_user =  UserRepo.create_user(db=db, user=user)
    logger.info(f"User '{created_user.email}' created successfully with ID {created_user.id}")
    return created_user

# Login user
def login_user(db:Session,user : UserSchema.UserLogin):
    found_user = authenticate_user(db,user.email,user.password)

    if not found_user:
        logger.warning(f"Login failed for email '{user.email}'")
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
    logger.info(f"User '{found_user.email}' logged in successfully")
    return UserSchema.UserLoginResponse(token=token,user=UserSchema.User(**data))