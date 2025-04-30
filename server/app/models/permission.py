from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base

class Permission(Base):
    __tablename__ = "permissions"  # Explicitly set the table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_type = Column(String(255), nullable=False)
    granted = Column(Boolean, nullable=False)
    granted_to = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    granted_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    granted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Define relationships with the Admin table
    granted_to_user = relationship("User", foreign_keys=[granted_to], back_populates="permissions_granted_to")
    granted_by_user = relationship("User", foreign_keys=[granted_by], back_populates="permissions_granted_by")
