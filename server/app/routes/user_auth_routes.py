from fastapi import APIRouter, Depends
import services.users.google_auth_service as GoogleAuthService
import services.users.facebook_auth_service as FacebookAuthService
from sqlalchemy.orm import Session
from db.database import get_db
import schemas.user as UserSchema
from dependencies.auth_dep import restrict_authenticated_users,get_nonadmin_user

router = APIRouter(prefix="/user/auth",tags=["User - Auth"])

@router.post("/login/google",dependencies=[Depends(restrict_authenticated_users)],response_model=UserSchema.UserLoginResponse)
def login_by_google(data: UserSchema.GoogleAuthRequest, db : Session = Depends(get_db)):
    return GoogleAuthService.login_by_google(data=data,db=db)

@router.post("/login/facebook",dependencies=[Depends(restrict_authenticated_users)],response_model=UserSchema.UserLoginResponse)
def login_by_facebook(data: UserSchema.FacebookAuthRequest,db:Session = Depends(get_db)):
    return FacebookAuthService.login_by_facebook(data=data,db=db)

@router.post("/verify",response_model=UserSchema.User)
async def verify_nonadmin_user(user : UserSchema.User = Depends(get_nonadmin_user)):
    return user