from fastapi import APIRouter,Depends
import dependencies.auth_dep as AuthDependency
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.auditlog import AuditLog
from typing import List
import services.admin.auditlog_service as AuditLogService
from enums.Roles import Roles

router = APIRouter(
    prefix="/admin/auditlog",
    tags=["Admin"],
    dependencies=[
        Depends(AuthDependency.allow_roles_to_admin([Roles.SUPER_ADMIN,Roles.AUDITOR]))
    ]
)

@router.get("/",
    response_model=List[AuditLog]
)
async def get_all_auditlogs(db:Session = Depends(get_db)):
    return AuditLogService.get_all_auditlogs(db=db)

@router.get("/{log_id}",
    response_model=AuditLog
)
async def get_specific_auditlog(log_id: int,db:Session = Depends(get_db)):
    return AuditLogService.get_specific_auditlog(db=db,log_id=log_id)

@router.get("/user/{user_id}",response_model=List[AuditLog])
async def get_specific_admin_auditlog(user_id:int,db:Session=Depends(get_db)):
    return AuditLogService.get_specific_admin_auditlog(db=db,user_id=user_id)