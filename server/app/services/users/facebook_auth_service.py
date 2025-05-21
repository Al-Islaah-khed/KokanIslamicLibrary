import requests
from fastapi import HTTPException, status
from config import Settings
from sqlalchemy.orm import Session
from schemas.user import FacebookAuthRequest, AdminLoginResponse, UserCreate
from helpers.token import generate_token
from datetime import timedelta
from enums.AuthProvider import AuthProvider
from repositories.user_repo import UserRepo
from helpers.converters import UserModel_to_Schema
from helpers.logger import logger

settings = Settings()

def login_by_facebook(data: FacebookAuthRequest, db: Session):
    try:
        logger.info("Verifying Facebook access token")
        fb_url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={data.access_token}"
        resp = requests.get(fb_url)
        fb_data = resp.json()

        if "error" in fb_data or not fb_data.get("email"):
            raise HTTPException(status_code=401, detail="Invalid Facebook access token")

        email = fb_data["email"]
        fullname = fb_data["name"]
        profile_image = fb_data["picture"]["data"]["url"]
        provider_id = fb_data["id"]

        logger.debug(f"Facebook user: {email} - {fullname}")

        found_user = UserRepo.get_user_by_email(db=db, email=email)

        if found_user and found_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin cannot login via Facebook")

        if not found_user:
            user = UserCreate(
                fullname=fullname,
                email=email,
                profile_image=profile_image,
                auth_provider=AuthProvider.FACEBOOK,
                provider_id=provider_id,
            )
            found_user = UserRepo.create_nonadmin_user(db=db, user=user)

        UserRepo.update_last_login(db=db, user=found_user)

        user_data = UserModel_to_Schema(found_user)

        token = generate_token(
            data=user_data.model_dump(mode="json"),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        logger.info(f"Facebook login successful for user {email}")
        return AdminLoginResponse(token=token, user=UserModel_to_Schema(found_user))

    except Exception as e:
        logger.error(f"Facebook login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Facebook login failed")
