from fastapi import APIRouter,Depends
import dependencies.auth_dep as AuthDependency
import schemas.role as RoleSchema
import services.admin.user_service as AdminUserService
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter(prefix="/admin/users", tags=["Admin"])

@router.post("/{user_id}/roles",
    response_model = RoleSchema.AssignResponse,
    dependencies=[Depends(AuthDependency.allow_roles_to_admin(["super_admin"]))]
)
async def assign_role_to_user(
    user_id:int,
    role : RoleSchema.AssignRole,
    db: Session = Depends(get_db),
):
    return AdminUserService.assign_role_to_user(user_id,role,db)

@router.delete("/{user_id}/roles",
            response_model=RoleSchema.AssignResponse,
            dependencies=[Depends(AuthDependency.allow_roles_to_admin(["super_admin"]))]
)
async def remove_role_from_user(
    user_id : int,
    role : RoleSchema.AssignRole,
    db : Session = Depends(get_db),

):
    return AdminUserService.remove_role_from_user(user_id,role,db)