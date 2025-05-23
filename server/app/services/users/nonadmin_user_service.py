from Sqlalchemy.orm import Session
from fastapi import HTTPException,status
from repositories.user_repo import UserRepo
from helpers.converters import UserModel_to_Schema
from helpers.logger import logger
import traceback

def get_specific_nonadmin_user(user_id: int, db: Session):
    logger.info(f"Fetching non-admin user with ID: {user_id}")
    try:
        user = UserRepo.get_user_by_id(db=db,user_id=user_id,is_admin=False)

        if not user:
            logger.warning(f"No non-admin user found with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found for specified id"
            )

        logger.info(f"Successfully fetched non-admin user with ID: {user_id}")
        return UserModel_to_Schema(user)

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        raise

    except Exception as e:
        logger.exception("Unexpected error occurred while fetching non-admin user")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user"
        )