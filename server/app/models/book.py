from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
from .category import book_categories

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    isbn = Column(String(255), nullable=True)
    author = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    is_digital = Column(Boolean, nullable=False)
    cover_image = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    is_approved = Column(Boolean, nullable=False)
    is_restricted = Column(Boolean, nullable=False)

    book_pdf_string = Column(String(255), nullable=True)
    book_pdf_content = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    categories = relationship("Category", secondary=book_categories, back_populates="books")
    subcategories = relationship("SubCategory", secondary=book_categories, back_populates="books")
    digital_access = relationship("DigitalAccess", back_populates="book")

    copies = relationship("BookCopy", back_populates="book", cascade="all, delete-orphan")

    upload_requests = relationship("BookUploadRequest", back_populates="book", cascade="all, delete-orphan")