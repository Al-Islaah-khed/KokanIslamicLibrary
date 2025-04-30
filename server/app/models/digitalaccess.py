from db.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from sqlalchemy.orm import relationship

class DigitalAccess(Base):
    __tablename__ = "digital_accesses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    access_granted = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="digital_access")
    book = relationship("Book", back_populates="digital_access")