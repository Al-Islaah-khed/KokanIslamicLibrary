from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False)
    shelf_number = Column(String(20), nullable=False)
    section_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    # Optional timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to BookCopy
    copies = relationship("BookCopy", back_populates="location", cascade="all, delete-orphan")

    # 🔁 Historical book-copy relationships
    book_locations = relationship("BookLocation", back_populates="location", cascade="all, delete-orphan")