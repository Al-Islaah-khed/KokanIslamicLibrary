from sqlalchemy import Column, Integer, String, Text,ForeignKey,Table
from sqlalchemy.orm import relationship
from db.database import Base

book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("subcategory_id", Integer, ForeignKey("subcategories.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    subcategories = relationship("SubCategory", back_populates="category", cascade="all, delete-orphan")
    books = relationship("Book", secondary=book_categories, back_populates="categories")