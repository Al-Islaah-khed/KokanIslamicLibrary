from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from db.database import Base
from enums.TargetType import TargetType

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_id = Column(Integer, nullable=True)
    target_type = Column(SqlEnum(TargetType), nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    description = Column(Text, nullable=False)
    ip_address = Column(String(100),nullable=False)
    user_agent = Column(String(255),nullable=False)

    user = relationship("User", back_populates="action_performed")