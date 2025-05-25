from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Request
from repositories.user_repo import UserRepo
from helpers.converters import UserModel_to_Schema
from helpers.logger import logger
import traceback

def get_specific_nonadmin_user(request:Request,user_id: int, db: Session):
    logger.info(f"[USER_ACCESS] Attempt to fetch non-admin user with ID: {user_id}")
    try:
        current_user = request.state.user

        # i know it cannot be none but for safety added extra condition
        if not current_user:
            logger.warning(f"[USER_ACCESS_DENIED] No user found in request state")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User authentication required"
            )

        if current_user.id != user_id:
            logger.warning(
                f"[USER_ACCESS_DENIED] User ID {current_user.id} attempted to access user ID {user_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: you do not own this account"
            )

        user = UserRepo.get_user_by_id(db=db,user_id=user_id,is_admin=False)

        if not user:
            logger.warning(f"[USER_NOT_FOUND] No non-admin user found with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found for the specified ID"
            )

        logger.info(f"[USER_ACCESS_GRANTED] Non-admin user with ID {user_id} successfully fetched")
        return UserModel_to_Schema(user)

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"[UNEXPECTED_ERROR] Unexpected error while fetching user ID {user_id}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user"
        )