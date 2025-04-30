from db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum, DateTime,func 
from sqlalchemy.orm import relationship
from datetime import datetime
from enums.BookCopyStatus import BookCopyStatus


class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    status = Column(SqlEnum(BookCopyStatus), nullable=False)

    added_by = Column(Integer, ForeignKey("users.id"))

    # Optional timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    book = relationship("Book", back_populates="copies")
    location = relationship("Location", back_populates="copies")
    
    added_by_user = relationship("User",back_populates="added_book_copies")
    
    issued_details = relationship("IssuedBook",back_populates="issued_bookcopy")
    
    # 🔁 Historical locations
    location_history = relationship("BookLocation", back_populates="book_copy", cascade="all, delete-orphan")