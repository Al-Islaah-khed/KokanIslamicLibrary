from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Enum as SqlEnum
from enums.AuthProvider import AuthProvider

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
    password = Column(String(255), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # details only provided by the google or facebook

    profile_image = Column(String(255),nullable=True)
    phone_no = Column(String(15),nullable=True)
    auth_provider = Column(SqlEnum(AuthProvider),nullable=True,default=AuthProvider.LOCAL)
    provider_id = Column(String(255),nullable=True)

    # timing details
    last_login = Column(DateTime(timezone=True),nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # relationships
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

    def __repr__(self):
        return f"<User id={self.id} email={self.email} provider={self.auth_provider}>"