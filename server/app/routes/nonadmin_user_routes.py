from fastapi import APIRouter,Depends,Request,UploadFile,File,Form
import schemas.user as UserSchema
from db.database import get_db
from sqlalchemy.orm import Session
import services.users.nonadmin_user_service as NonAdminUserService
from dependencies.auth_dep import allow_roles_to_user
from typing import Optional

router = APIRouter(prefix="/user",
        tags=["User"],
        dependencies=[Depends(allow_roles_to_user([]))]
)

@router.get("/{user_id}",response_model=UserSchema.User)
def get_specific_nonadmin_user(request:Request,user_id: int,db:Session = Depends(get_db)):
    return NonAdminUserService.get_specific_nonadmin_user(request=request,user_id=user_id,db=db)

@router.put("/users/{user_id}",response_model=UserSchema.User)
async def update_nonadmin_user(
    request: Request,
    user_id: int,
    fullname: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    return NonAdminUserService.update_nonadmin_user(
        request=request,
        user_id=user_id,
        db=db,
        fullname=fullname,
        is_active=is_active,
        profile_image=profile_image,
    )