from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base

class BookLocation(Base):
    __tablename__ = "book_locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    book_copy_id = Column(Integer, ForeignKey("book_copies.id"), nullable=False)

    # Optional: track when the copy was moved to this location
    moved_at = Column(DateTime(timezone=True), default=func.now())

    # Relationships
    location = relationship("Location", back_populates="book_locations")
    book_copy = relationship("BookCopy", back_populates="location_history")
