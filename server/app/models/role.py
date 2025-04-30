from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
from .user import user_roles  # import the association table

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    # Many-to-many relationship
    users = relationship("User", secondary=user_roles, back_populates="roles")