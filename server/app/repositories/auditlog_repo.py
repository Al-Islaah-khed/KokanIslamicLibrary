from models.auditlog import AuditLog
import schemas.auditlog as AuditLogSchema
from sqlalchemy.orm import Session
from typing import List,Optional

class AuditLogRepo():

    def create_auditlog(db: Session, auditlog: AuditLogSchema.AuditLogCreate ) -> AuditLog :
        new_log = AuditLog(
            action_by = auditlog.action_by,
            target_id = auditlog.target_id,
            target_type = auditlog.target_type,
            description = auditlog.description,
            ip_address = auditlog.ip_address,
            user_agent = auditlog.user_agent
        )

        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log

    def get_all_logs(db: Session) -> List[AuditLog]:
        return db.query(AuditLog).all()

    def find_log_by_id(db: Session, log_id: int) -> Optional[AuditLog]:
        return db.query(AuditLog).filter(AuditLog.id == log_id).first()