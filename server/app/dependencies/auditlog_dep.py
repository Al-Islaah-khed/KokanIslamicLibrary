from fastapi import Request, Depends
from sqlalchemy.orm import Session
import dependencies.auth_dep as AuthDependency
import services.admin.auditlog_service as AuditLogService
from enums.TargetType import TargetType
from db.database import get_db
import schemas.user as UserSchema

def get_audit_logger(
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserSchema.Admin = Depends(AuthDependency.get_admin)
):
    def log_action(
        description: str,
        target_id: int | None = None,
        target_type: TargetType | None = None,
    ):
        return AuditLogService.create_log(
            db=db,
            action_by=current_user.id,
            description=description,
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            target_id=target_id,
            target_type=target_type
        )

    return log_action