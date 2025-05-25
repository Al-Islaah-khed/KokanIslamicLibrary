from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
import services.admin.auth_service as AuthService
from dependencies.auth_dep import restrict_authenticated_users,get_admin
from db.database import get_db
from schemas.user import Admin,AdminCreate,AdminLogin,AdminLoginResponse

router = APIRouter(prefix="/admin/auth",tags=["Admin - Auth"])

@router.post("/register",
            response_model=Admin,
            dependencies=[Depends(restrict_authenticated_users)]

)
async def register_admin(
    user : AdminCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register_admin(db=db,user=user)

@router.post("/login",
    response_model=AdminLoginResponse,
    dependencies=[Depends(restrict_authenticated_users)]
)
async def login_admin(
    user : AdminLogin,
    db: Session = Depends(get_db),
):
    return AuthService.login_admin(db=db,user=user)

@router.post("/verify",response_model=Admin)
async def verify_admin(admin : Admin = Depends(get_admin)):
    return admin