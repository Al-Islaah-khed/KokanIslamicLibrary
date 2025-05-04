from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
import services.auth_service as AuthService
import dependencies.auth_dep as AuthDependency
from db.database import get_db
from schemas.user import User,UserCreate,UserLogin,UserLoginResponse

router = APIRouter(prefix="/admin/auth",tags=["Admin"])

@router.post("/register",
            response_model=User,
            dependencies=[Depends(AuthDependency.restrict_authenticated_users)]

)
async def register(
    user : UserCreate,
    db : Session = Depends(get_db),
):
    return AuthService.create_user(db=db,user=user)

@router.post("/login",
    response_model=UserLoginResponse,
    dependencies=[Depends(AuthDependency.restrict_authenticated_users)]
)
async def login(
    user : UserLogin,
    db: Session = Depends(get_db),
):
    return AuthService.login_user(db=db,user=user)

@router.post("/verify",response_model=User)
async def verify_user(admin : User = Depends(AuthDependency.get_admin)):
    return admin