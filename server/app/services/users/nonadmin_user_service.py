from fastapi import HTTPException,status,Request,UploadFile,File
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepo
from helpers.converters import UserModel_to_Schema
from helpers.logger import logger
from pathlib import Path
from typing import Optional
from helpers.uploads import upload_image

import schemas.user as UserSchema


UPLOAD_DIR = Path("public/uploads/profile-images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def ensure_user_ownership(request: Request, target_user_id: int):
    current_user = request.state.user

    # i know it cannot be none but for safety added extra condition
    if not current_user:
            logger.warning(f"[USER_ACCESS_DENIED] No user found in request state")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User authentication required"
            )

    if current_user.id != target_user_id:
        logger.warning(
                f"[USER_ACCESS_DENIED] User ID {current_user.id} attempted to access user ID {target_user_id}"
        )
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: you do not own this account"
        )
    return current_user

def get_specific_nonadmin_user(request:Request,user_id: int, db: Session):
    logger.info(f"[USER_ACCESS] Attempt to fetch non-admin user with ID: {user_id}")
    try:

        ensure_user_ownership(request, user_id)

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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user"
        )


def update_nonadmin_user(request: Request, user_id: int, db: Session, fullname: Optional[str] = None, is_active: Optional[bool] = None, profile_image: UploadFile = File(None)):
    logger.info(f"[USER_UPDATE] Attempt to update user with ID: {user_id}")
    try:
        ensure_user_ownership(request, user_id)

        new_profile_image = None

        if profile_image is not None:
            new_profile_image =  new_profile_image = upload_image(
                upload_dir=UPLOAD_DIR,
                file=profile_image,
                base_url=str(request.base_url).rstrip("/")
            )

        user_data = UserSchema.UserUpdate(
            fullname=fullname,
            is_active=is_active,
            profile_image=new_profile_image
        )

        updated_user = UserRepo.update_nonadmin_user(db=db,user_id=user_id,user_data=user_data)

        logger.info(f"[USER_UPDATED] User ID {user_id} updated successfully")

        return UserModel_to_Schema(updated_user)

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"[UNEXPECTED_ERROR] Error while updating user ID {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the user"
        )
