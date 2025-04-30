from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from enums.bookuploadstauts import BookUploadStatus
from db.database import Base

class BookUploadRequest(Base):
    __tablename__ = "book_upload_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=True)

    status = Column(SqlEnum(BookUploadStatus), nullable=False)
    submitted_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    remarks = Column(Text, nullable=True)

    # Relationships
    submitter = relationship("User", foreign_keys=[submitted_by], back_populates="submitted_uploads")
    reviewer = relationship("User", foreign_keys=[reviewed_by], back_populates="reviewed_uploads")
    book = relationship("Book", back_populates="upload_requests")
