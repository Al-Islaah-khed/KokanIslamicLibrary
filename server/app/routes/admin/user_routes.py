from fastapi import APIRouter,Depends
import dependencies.auth_dep as AuthDependency
import schemas.role as RoleSchema
import services.admin.user_service as AdminUserService
from sqlalchemy.orm import Session
from db.database import get_db
import dependencies.auditlog_dep as AuditLogDependency
from enums.Roles import Roles
import schemas.user as UserSchema
from typing import List,Union
from schemas.response import APIResponse

router = APIRouter(prefix="/admin/users",
    tags=["Admin"],
    dependencies=[Depends(AuthDependency.allow_roles_to_admin(
        [Roles.SUPER_ADMIN,Roles.STAFF_ADMIN]
    )
    )]
)

# user's operations like crud related routes

@router.post("/",response_model=UserSchema.Admin)
async def create_new_admin(
    user : UserSchema.AdminCreate,
    db : Session = Depends(get_db),
    create_auditlog = Depends(AuditLogDependency.get_audit_logger)
):
    return AdminUserService.create_admin(db=db,user=user,create_auditlog=create_auditlog)

@router.get("/",response_model = List[Union[UserSchema.Admin, UserSchema.User]])
async def get_all_users(
    db : Session = Depends(get_db),
    is_admin: bool | None = None
):
    return AdminUserService.get_all_users(
        db=db,
        is_admin=is_admin
    )

@router.get("/{user_id}",response_model=UserSchema.Admin | UserSchema.User)
async def get_specific_user(
    user_id : int,
    db:Session = Depends(get_db),
    is_admin: bool | None = None
):
    return AdminUserService.get_specific_user(
        db=db,
        user_id=user_id,
        is_admin=is_admin
    )

@router.put("/{user_id}",response_model=UserSchema.Admin)
async def update_admin(
    user_id:int,
    user_data :UserSchema.AdminUpdate,
    db : Session = Depends(get_db),
    create_auditlog = Depends(AuditLogDependency.get_audit_logger)
):
    return AdminUserService.update_admin(
        db=db,
        user_id=user_id,
        user_data=user_data,
        create_auditlog=create_auditlog
    )

@router.delete("/{user_id}" , response_model=APIResponse)
async def delete_admin(
    user_id : int,
    db : Session = Depends(get_db),
    create_auditlog = Depends(AuditLogDependency.get_audit_logger),
    current_admin : UserSchema.Admin = Depends(AuthDependency.get_admin)
):
    return AdminUserService.delete_admin(
        db=db,
        user_id=user_id,
        create_auditlog=create_auditlog,
        current_admin=current_admin
    )

# user role related routes

@router.post("/{user_id}/roles",
    response_model = RoleSchema.AssignResponse,
)
async def assign_role_to_user(
    user_id:int,
    role : RoleSchema.AssignRole,
    db: Session = Depends(get_db),
    create_auditlog = Depends(AuditLogDependency.get_audit_logger)
):
    return AdminUserService.assign_role_to_user(
        user_id=user_id,
        role=role,
        db=db,
        create_auditlog=create_auditlog
    )

@router.delete("/{user_id}/roles",
            response_model=RoleSchema.AssignResponse,
)
async def remove_role_from_user(
    user_id : int,
    role : RoleSchema.AssignRole,
    db : Session = Depends(get_db),
    create_auditlog = Depends(AuditLogDependency.get_audit_logger)
):
    return AdminUserService.remove_role_from_user(user_id,role,db,create_auditlog=create_auditlog)