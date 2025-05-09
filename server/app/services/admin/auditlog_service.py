from sqlalchemy.orm import Session
import schemas.auditlog as AuditLogSchema
from repositories.auditlog_repo import AuditLogRepo
from fastapi import  HTTPException,status
from helpers.converters import AuditLogModel_to_Schema

def create_log(
        db: Session,
        action_by: int,
        description: str,
        ip_address: str,
        user_agent: str,
        target_id: int | None = None,
        target_type = None,
):
    auditlog = AuditLogSchema.AuditLogCreate(
        action_by=action_by,
        target_id=target_id,
        target_type=target_type,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    try:
        created_log = AuditLogRepo.create_auditlog(db=db, auditlog=auditlog)
    except:
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            details=f"Error occured while creating auditlog"
        )

    return AuditLogModel_to_Schema(created_log)

def get_all_auditlogs(db: Session):
    logs =  AuditLogRepo.get_all_logs(db=db)
    return [AuditLogModel_to_Schema(log) for log in logs]

def get_specific_auditlog(db:Session,log_id):
    log = AuditLogRepo.find_log_by_id(db=db,log_id=log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit log with ID {log_id} not found"
        )

    return AuditLogModel_to_Schema(log)
