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

def login_by_google(data: UserSchema.GoogleAuthRequest, db: Session) -> UserSchema.User:
    try:
        logger.info("[GOOGLE_LOGIN_START] Google login flow initiated")

        # Step 1: Verify Google ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                data.id_token, GoogleRequest.Request(), settings.GOOGLE_CLIENT_ID
            )
            logger.info("[GOOGLE_TOKEN_VERIFIED] Google ID token verified successfully")
        except ValueError as ve:
            logger.warning(f"[GOOGLE_TOKEN_INVALID] ID token verification failed: {str(ve)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google ID token"
            )

        # Step 2: Extract user info
        email = idinfo.get('email')
        fullname = idinfo.get('name')
        profile_image = idinfo.get('picture')
        provider_id = idinfo.get('sub')

        logger.debug(
            f"[GOOGLE_USER_INFO] Extracted info: email={email}, name={fullname}, provider_id={provider_id}"
        )

        if not email or not fullname or not provider_id:
            logger.error("[GOOGLE_USER_INFO_MISSING] Missing required data from Google token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required user information from Google"
            )

        # Step 3: Check if user already exists
        found_user = UserRepo.get_user_by_email(db=db, email=email)

        if found_user and found_user.is_admin:
            logger.warning(f"[GOOGLE_LOGIN_ADMIN_BLOCKED] Admin email login blocked: {email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied as this is an admin email"
            )

        # Step 4: Create user if not found
        if not found_user:
            logger.info(f"[GOOGLE_USER_CREATE] Creating new user for {email}")
            user = UserSchema.UserCreate(
                fullname=fullname,
                email=email,
                profile_image=profile_image,
                auth_provider=AuthProvider.GOOGLE,
                provider_id=provider_id
            )
            found_user = UserRepo.create_nonadmin_user(db=db, user=user)
            logger.info(f"[GOOGLE_USER_CREATED] User created successfully: {email}")

        # Step 5: Generate and return token
        UserRepo.update_last_login(db=db, user=found_user)
        logger.info(f"[GOOGLE_USER_LAST_LOGIN_UPDATED] Last login timestamp updated for {email}")

        token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        user_data = UserModel_to_Schema(found_user)

        token = generate_token(data=user_data.model_dump(mode="json"), expires_delta=token_expires)
        logger.info(f"[GOOGLE_LOGIN_SUCCESS] Token issued and login completed for {email}")

        return UserSchema.UserLoginResponse(token=token, user=user_data)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"[GOOGLE_LOGIN_ERROR] Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while logging in"
        )
