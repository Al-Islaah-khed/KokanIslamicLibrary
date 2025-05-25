from sqlalchemy.orm import Session
import schemas.auditlog as AuditLogSchema
from repositories.auditlog_repo import AuditLogRepo
from fastapi import  HTTPException,status
from helpers.converters import AuditLogModel_to_Schema
from helpers.logger import logger
from typing import Optional
import traceback

def create_log(
        db: Session,
        action_by: int,
        description: str,
        ip_address: str,
        user_agent: str,
        target_id: Optional[int] = None,
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
        logger.info(f"[AUDITLOG_CREATE_START] Attempting to create audit log: action_by={action_by}, target_id={target_id}, target_type={target_type}")
        created_log = AuditLogRepo.create_auditlog(db=db, auditlog=auditlog)
        logger.info(f"[AUDITLOG_CREATE_SUCCESS] Audit log created successfully by user {action_by}")

    except Exception as e:
        logger.error(f"[AUDITLOG_CREATE_ERROR] Error while creating audit log by user {action_by}: {str(e)}")
        logger.error(f"[AUDITLOG_CREATE_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            details=f"Error occured while creating auditlog"
        )

    return AuditLogModel_to_Schema(created_log)


def get_all_auditlogs(db: Session):
    try:
        logger.info("[AUDITLOG_FETCH_ALL_START] Attempting to fetch all audit logs")
        logs =  AuditLogRepo.get_all_logs(db=db)
        logger.info(f"[AUDITLOG_FETCH_ALL_SUCCESS] Retrieved {len(logs)} audit logs")
        return [AuditLogModel_to_Schema(log) for log in logs]
    except HTTPException:
        logger.warning("[AUDITLOG_FETCH_ALL_HTTP_ERROR] Known HTTP exception encountered while fetching audit logs")
        raise
    except Exception as e:
        logger.error(f"[AUDITLOG_FETCH_ALL_ERROR] Unexpected error while fetching audit logs: {str(e)}")
        logger.error(f"[AUDITLOG_FETCH_ALL_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching all auditlogs"
        )


def get_specific_auditlog(db:Session, log_id: int):
    try:
        logger.info(f"[AUDITLOG_FETCH_ONE_START] Attempting to fetch audit log with ID: {log_id}")
        log = AuditLogRepo.find_log_by_id(db=db, log_id=log_id)
        if not log:
            logger.warning(f"[AUDITLOG_FETCH_ONE_NOT_FOUND] Audit log with ID {log_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Audit log with ID {log_id} not found"
            )

        logger.info(f"[AUDITLOG_FETCH_ONE_SUCCESS] Audit log with ID {log_id} fetched successfully")
        return AuditLogModel_to_Schema(log)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[AUDITLOG_FETCH_ONE_ERROR] Unexpected error while fetching audit log ID {log_id}: {str(e)}")
        logger.error(f"[AUDITLOG_FETCH_ONE_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching specific auditlog"
        )


def get_specific_admin_auditlog(db:Session, user_id: int):
    try:
        logger.info(f"[AUDITLOG_FETCH_BY_ADMIN_START] Fetching audit logs for admin user ID: {user_id}")
        logs = AuditLogRepo.find_log_by_user_id(db=db, user_id=user_id)

        logger.info(f"[AUDITLOG_FETCH_BY_ADMIN_SUCCESS] Retrieved {len(logs)} logs for admin user {user_id}")
        return [AuditLogModel_to_Schema(log) for log in logs]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[AUDITLOG_FETCH_BY_ADMIN_ERROR] Unexpected error while fetching logs for admin user {user_id}: {str(e)}")
        logger.error(f"[AUDITLOG_FETCH_BY_ADMIN_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching specific admin auditlogs"
        )