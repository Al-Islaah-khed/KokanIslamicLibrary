from fastapi import HTTPException,Depends,Request,status
from sqlalchemy.orm import Session
from models.user import User
from db.database import get_db
from helpers.token import verify_token,is_token_available,decode_token
from repositories.user_repo import UserRepo
from typing import List
from jose import JWTError
import schemas.user as UserSchema
from helpers.logger import logger

# restrict loggedin users
async def restrict_authenticated_users(token: str = Depends(is_token_available)):
    if token:
        try:
            payload = decode_token(token)
            if payload:
                logger.warning("Attempt to access restricted route while already logged in")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You are already logged in"
                )
        except JWTError as e:
            logger.warning(f"JWT decode error: {str(e)}")
            pass

# Get current user from database
async def get_current_user(
    request : Request,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token),
):

    if hasattr(request.state, "user"):
        logger.info("User retrieved from request state cache")
        return request.state.user

    email = payload.get("email")
    if not email:
        logger.error("Token does not contain email")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing email information"
        )

    user = UserRepo.get_user_by_email(db, email)
    if not user:
        logger.warning(f"User with email '{email}' not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    role_names = [role.name for role in user.roles]
    user_dict = user.__dict__
    user_dict['roles'] = role_names
    user_data = UserSchema.User(**user_dict)

    request.state.user = user_data
    logger.info(f"Authenticated user '{email}' with roles: {role_names}")
    return user_data

# Check if current user is active
async def get_current_active_user(
    current_user: UserSchema.User = Depends(get_current_user)
):
    if not current_user.is_active:
        logger.warning(f"Inactive user '{current_user.email}' attempted to access")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# check user is admin
async def get_admin(
    active_user: UserSchema.User = Depends(get_current_active_user)
):
    if not active_user.is_admin:
        logger.warning(f"Non-admin user '{active_user.email}' tried to access admin route")
        raise HTTPException(status_code=403, detail="Not an admin")
    logger.info(f"Admin access granted to user '{active_user.email}'")
    return active_user


# check user is not an admin
async def get_normal_user(
    active_user: UserSchema.User = Depends(get_current_active_user)
):
    if active_user.is_admin:
        logger.warning(f"Admin user '{active_user.email}' tried to access normal user route")
        raise HTTPException(status_code=403,detail="Access denied")
    logger.info(f"Normal user access granted to '{active_user.email}'")
    return active_user

# authenticate normal user role
def allow_roles(allowed_roles: List[str]):
    def role_checker(user: UserSchema.User = Depends(get_current_active_user)):
        if not any(role in allowed_roles for role in user.roles):
            logger.warning(f"User '{user.email}' denied access due to insufficient roles")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        logger.info(f"User '{user.email}' granted access with role(s): {user.roles}")
        return user
    return role_checker

# authenticate admin user role
def allow_roles_to_admin(allowed_roles: List[str]):
    def role_checker(user: User = Depends(get_admin)):
        if not any(role in allowed_roles for role in user.roles):
            logger.warning(f"Admin '{user.email}' denied access due to missing roles")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        logger.info(f"Admin '{user.email}' granted access with role(s): {user.roles}")
        return user
    return role_checker