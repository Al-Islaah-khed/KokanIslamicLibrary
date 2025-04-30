from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from db.database import Base
from enums.ActionByType import ActionByType
from enums.TargetType import TargetType

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_by_type = Column(SqlEnum(ActionByType), nullable=False)
    target_id = Column(Integer, nullable=False)
    target_type = Column(SqlEnum(TargetType), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    description = Column(Text, nullable=False)

    user = relationship("User", foreign_keys=[action_by], back_populates="action_performed")