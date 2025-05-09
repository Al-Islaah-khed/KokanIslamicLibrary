from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Many-to-many relationship with roles
    roles = relationship("Role", secondary=user_roles, back_populates="users",passive_deletes=True)

    # Permissions granted to or by the user
    permissions_granted_to = relationship("Permission", foreign_keys="[Permission.granted_to]", back_populates="granted_to_user")
    permissions_granted_by = relationship("Permission", foreign_keys="[Permission.granted_by]", back_populates="granted_by_user")

    # Audit logs performed by the user (if admin)
    action_performed = relationship("AuditLog", back_populates="user")

    # Digital Access Relationship
    digital_access = relationship("DigitalAccess", back_populates="user")

    added_book_copies = relationship("BookCopy", back_populates="added_by_user")
    
    issued_books = relationship("IssuedBook",back_populates="issued_to")

    submitted_uploads = relationship("BookUploadRequest", back_populates="submitter", foreign_keys="[BookUploadRequest.submitted_by]")
    reviewed_uploads = relationship("BookUploadRequest", back_populates="reviewer", foreign_keys="[BookUploadRequest.reviewed_by]")