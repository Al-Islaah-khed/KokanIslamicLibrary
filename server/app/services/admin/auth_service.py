from sqlalchemy.orm import Session
from fastapi import  HTTPException, status

from repositories.user_repo import UserRepo
from helpers.password_hash import get_password_hash,verify_password
from helpers.token import generate_token
import schemas.user as UserSchema
from datetime import timedelta
from helpers.logger import logger
from helpers.converters import UserModel_to_AdminSchema
import traceback

from config import Settings

settings = Settings()

# Authenticate user
def authenticate_admin_user(db: Session, email: str, password: str) -> UserSchema.Admin:
    logger.info(f"[AUTH_ADMIN_START] Authenticating admin user with email: '{email}'")
    admin = UserRepo.get_user_by_email(db=db, email=email, is_admin=True)
    if not admin:
        logger.warning(f"[AUTH_ADMIN_FAIL] Admin with email '{email}' not found")
        return None
    if not verify_password(password, admin.password):
        logger.warning(f"[AUTH_ADMIN_FAIL] Incorrect password for admin '{email}'")
        return None
    logger.info(f"[AUTH_ADMIN_SUCCESS] Admin '{email}' authenticated successfully")
    return admin

# Create User
def register_admin(db: Session, user: UserSchema.AdminCreate) -> UserSchema.Admin:
    try:
        logger.info(f"[REGISTER_ADMIN_START] Attempting to register admin with email: '{user.email}'")
        existing_user = UserRepo.get_user_by_email(db, user.email, is_admin=True)
        if existing_user:
            logger.warning(f"[REGISTER_ADMIN_FAIL] Email '{user.email}' already registered as admin")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user.password = get_password_hash(user.password)
        registered_admin = UserRepo.create_admin_user(db=db, user=user)
        logger.info(f"[REGISTER_ADMIN_SUCCESS] Admin '{registered_admin.email}' registered with ID {registered_admin.id}")

        return UserModel_to_AdminSchema(registered_admin)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[REGISTER_ADMIN_ERROR] Unexpected error during admin registration: {str(e)}")
        logger.error(f"[REGISTER_ADMIN_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while registering the admin"
        )

# Login user
def login_admin(db: Session, user: UserSchema.AdminLogin) -> UserSchema.AdminLoginResponse:
    try:
        logger.info(f"[LOGIN_ADMIN_START] Attempting login for admin with email: '{user.email}'")
        found_user = authenticate_admin_user(db=db, email=user.email, password=user.password)

        if not found_user:
            logger.warning(f"[LOGIN_ADMIN_FAIL] Login failed for email '{user.email}'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email and password")

        token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        data = UserModel_to_AdminSchema(found_user)

        UserRepo.update_last_login(db=db, user=found_user)

        token = generate_token(data=data.model_dump(mode="json"), expires_delta=token_expires)
        logger.info(f"[LOGIN_ADMIN_SUCCESS] Admin '{found_user.email}' logged in successfully")

        return UserSchema.AdminLoginResponse(token=token, user=data)
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        logger.error(f"[LOGIN_ADMIN_ERROR] Unexpected error during admin login: {str(e)}")
        logger.error(f"[LOGIN_ADMIN_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while logging in the admin"
        )