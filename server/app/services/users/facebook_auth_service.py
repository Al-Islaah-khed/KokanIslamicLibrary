import requests
from fastapi import HTTPException, status
from config import Settings
from sqlalchemy.orm import Session
from helpers.token import generate_token
from datetime import timedelta
from enums.AuthProvider import AuthProvider
from repositories.user_repo import UserRepo
from helpers.converters import UserModel_to_Schema
from helpers.logger import logger
import schemas.user as UserSchema

settings = Settings()

def login_by_facebook(data: UserSchema.FacebookAuthRequest, db: Session) -> UserSchema.User:
    try:
        logger.info("[FACEBOOK_LOGIN_START] Facebook login flow initiated")

        # Step 1: Verify Facebook Access Token and Fetch Profile Data
        logger.info("[FACEBOOK_TOKEN_VERIFY] Verifying Facebook access token")
        fb_url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={data.access_token}"
        resp = requests.get(fb_url)
        fb_data = resp.json()

        if "error" in fb_data or not fb_data.get("email"):
            logger.warning(f"[FACEBOOK_TOKEN_INVALID] Error fetching user info or email missing: {fb_data.get('error')}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Facebook access token")

        # Step 2: Extract and log user info
        email = fb_data["email"]
        fullname = fb_data["name"]
        profile_image = fb_data["picture"]["data"]["url"]
        provider_id = fb_data["id"]

        logger.debug(f"[FACEBOOK_USER_INFO] Extracted user info: email={email}, name={fullname}, provider_id={provider_id}")

        # Step 3: Admin check
        found_user = UserRepo.get_user_by_email(db=db, email=email)
        if found_user and found_user.is_admin:
            logger.warning(f"[FACEBOOK_LOGIN_ADMIN_BLOCKED] Admin email login blocked: {email}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin cannot login via Facebook")

        # Step 4: Create user if not found
        if not found_user:
            logger.info(f"[FACEBOOK_USER_CREATE] Creating new user for {email}")
            user = UserSchema.UserCreate(
                fullname=fullname,
                email=email,
                profile_image=profile_image,
                auth_provider=AuthProvider.FACEBOOK,
                provider_id=provider_id,
            )
            found_user = UserRepo.create_nonadmin_user(db=db, user=user)
            logger.info(f"[FACEBOOK_USER_CREATED] User created successfully: {email}")

        # Step 5: Update last login timestamp
        UserRepo.update_last_login(db=db, user=found_user)
        logger.info(f"[FACEBOOK_USER_LAST_LOGIN_UPDATED] Last login updated for user: {email}")

        # Step 6: Generate and return token
        user_data = UserModel_to_Schema(found_user)
        token = generate_token(
            data=user_data.model_dump(mode="json"),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        logger.info(f"[FACEBOOK_LOGIN_SUCCESS] Token issued and login successful for user: {email}")

        return UserSchema.UserLoginResponse(token=token, user=user_data)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"[FACEBOOK_LOGIN_ERROR] Unexpected error during Facebook login: {str(e)}")
        logger.error(f"[FACEBOOK_LOGIN_TRACEBACK]\n{e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Facebook login failed")
