from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
import services.auth_service as AuthService
from db.database import get_db
from schemas.user import User,UserCreate,UserLogin,UserLoginResponse

router = APIRouter()

@router.post("/register",response_model=User,tags=["Auth"])
async def register(user : UserCreate,db : Session = Depends(get_db)):
    return AuthService.create_user(db=db,user=user)

@router.post("/login",response_model=UserLoginResponse,tags=["Auth"])
async def login(user : UserLogin,db: Session = Depends(get_db)):
    return AuthService.login_user(db=db,user=user)

@router.post("/verify" , response_model=User,tags=["Auth"])
async def verify_user(current_user : User = Depends(AuthService.get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not an admin")
    return current_user