from sqlalchemy.orm import Session
import schemas.auditlog as AuditLogSchema
from repositories.auditlog_repo import AuditLogRepo
from fastapi import  HTTPException,status
from helpers.converters import AuditLogModel_to_Schema
from helpers.logger import logger
import traceback

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
        logger.info(f"Audit log created successfully by user {action_by}")

    except Exception as e:
        logger.error(f"Error occurred while creating audit log by user {action_by}: {str(e)}")
        logger.error(traceback.format_exc())

        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            details=f"Error occured while creating auditlog"
        )

    return AuditLogModel_to_Schema(created_log)

def get_all_auditlogs(db: Session):
    try:
        logs =  AuditLogRepo.get_all_logs(db=db)
        logger.info("Fetched all audit logs successfully.")
        return [AuditLogModel_to_Schema(log) for log in logs]
    except HTTPException:
        logger.warning("HTTPException occurred while fetching all audit logs.")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching all audit logs: {str(e)}")
        logger.error(traceback.format_exc())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching all auditlogs"
        )


def get_specific_auditlog(db:Session,log_id : int):
    try:
        log = AuditLogRepo.find_log_by_id(db=db,log_id=log_id)
        if not log:
            logger.warning(f"Audit log with ID {log_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Audit log with ID {log_id} not found"
            )

        logger.info(f"Audit log with ID {log_id} fetched successfully.")
        return AuditLogModel_to_Schema(log)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching audit log ID {log_id}: {str(e)}")
        logger.error(traceback.format_exc())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching specific auditlog"
        )

def get_specific_admin_auditlog(db:Session,user_id: int):
    try:
        logs = AuditLogRepo.find_log_by_user_id(db=db,user_id=user_id)

        logger.info(f"Audit logs for admin user {user_id} fetched successfully.")
        return [AuditLogModel_to_Schema(log) for log in logs]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching audit logs for admin user {user_id}: {str(e)}")
        logger.error(traceback.format_exc())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching specific admin auditlogs"
        )