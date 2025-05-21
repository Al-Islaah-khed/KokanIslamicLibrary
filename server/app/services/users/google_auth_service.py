from google.auth.transport import requests as GoogleRequest
from fastapi import HTTPException, status
from google.oauth2 import id_token
from config import Settings
import schemas.user as UserSchema
from repositories.user_repo import UserRepo
from sqlalchemy.orm import Session
from helpers.logger import logger
from enums.AuthProvider import AuthProvider
import traceback
from helpers.token import generate_token
from datetime import timedelta
from helpers.converters import UserModel_to_Schema

settings = Settings()

def login_by_google(data: UserSchema.GoogleAuthRequest, db: Session):
    try:
        logger.info("Starting Google login flow")

        # Step 1: Verify Google ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                data.id_token, GoogleRequest.Request(), settings.GOOGLE_CLIENT_ID
            )
            logger.info("Google ID token verified successfully")
        except ValueError as ve:
            logger.warning(f"Invalid Google ID token: {str(ve)}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google ID token")

        # Step 2: Extract required info
        email = idinfo.get('email')
        fullname = idinfo.get('name')
        profile_image = idinfo.get('picture')  # Correct key is 'picture'
        provider_id = idinfo.get('sub')  # 'sub' is the unique user ID from Google

        logger.debug(f"Extracted user info: email={email}, name={fullname}, provider_id={provider_id}")

        if not email or not fullname or not provider_id:
            logger.error("Missing required user data from Google ID token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required user information from Google"
            )

        # Step 3: Check if user exists
        found_user = UserRepo.get_user_by_email(db=db, email=email)

        if found_user and found_user.is_admin:
            logger.warning(f"Access denied: Admin trying to login via Google: {email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied as this is an admin email"
            )

        # Step 4: Create user if not found
        if not found_user:
            logger.info(f"New user. Creating non-admin user for {email}")
            user = UserSchema.UserCreate(
                fullname=fullname,
                email=email,
                profile_image=profile_image,
                auth_provider=AuthProvider.GOOGLE,
                provider_id=provider_id
            )
            found_user = UserRepo.create_nonadmin_user(db=db, user=user)
            logger.info(f"User created successfully for {email}")

        # Step 5: Issue token
        token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        user_data = UserModel_to_Schema(found_user)

        UserRepo.update_last_login(db=db, user=found_user)
        logger.info(f"Updated last login for user {email}")

        token = generate_token(data=user_data.model_dump(mode="json"), expires_delta=token_expires)
        logger.info(f"User '{email}' logged in successfully using Google login")

        return UserSchema.AdminLoginResponse(token=token, user=user_data)

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error during Google login for user. Error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while logging in"
        )
