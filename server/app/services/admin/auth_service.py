from sqlalchemy.orm import Session
from fastapi import  HTTPException, status

from repositories.user_repo import UserRepo
from helpers.password_hash import get_password_hash,verify_password
from helpers.token import generate_token
import schemas.user as UserSchema
from datetime import timedelta
from helpers.logger import logger
from helpers.converters import UserModel_to_AdminSchema

from config import Settings

settings = Settings()

# Authenticate user
def authenticate_admin_user(db: Session, email: str, password: str) -> UserSchema.Admin:
    admin = UserRepo.get_admin_user_by_email(db=db, email=email)
    if not admin:
        logger.warning(f"Authentication failed: admin with email '{email}' not found")
        return None
    if not verify_password(password, admin.password):
        logger.warning(f"Authentication failed: incorrect password for admin '{email}'")
        return None
    logger.info(f"Admin '{email}' authenticated successfully")
    return admin

# Create User
def register_admin(db: Session, user: UserSchema.AdminCreate) -> UserSchema.Admin:
    try:
        # if any user exists with the email either it is admin or non admin it's account cannot be created
        existing_user = UserRepo.get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"Admin registeration failed: email '{user.email}' already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user.password = get_password_hash(user.password)
        registered_admin =  UserRepo.create_admin_user(db=db, user=user)
        logger.info(f"Admin '{registered_admin.email}' registered successfully with ID {registered_admin.id}")

        return UserModel_to_AdminSchema(registered_admin)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during admin registeration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while registering the admin"
        )

# Login user
def login_admin(db:Session,user : UserSchema.AdminLogin) -> UserSchema.AdminLoginResponse:
    try:
        found_user = authenticate_admin_user(db=db,email=user.email,password=user.password)

        if not found_user:
            logger.warning(f"Login failed for email '{user.email}'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email and password")

        token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        # data = {
        #         "fullname" : found_user.fullname,
        #         "email":found_user.email,
        #         "id": found_user.id,
        #         "is_admin": found_user.is_admin,
        #         "is_active":found_user.is_active,
        # }

        # if found_user.roles:
        #     data["roles"] = [role.name for role in found_user.roles]

        data = UserModel_to_AdminSchema(found_user)

        UserRepo.update_last_login(db=db,user=found_user)

        token = generate_token(data=data.model_dump(),expires_delta=token_expires)
        logger.info(f"User '{found_user.email}' logged in successfully")
        return UserSchema.AdminLoginResponse(token=token,user=data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during admin login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while logging in the admin"
        )