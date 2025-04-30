from db.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from enums.IssuedBookStatus import IssuedBookStatus

class IssuedBook(Base):

    __tablename__ = "issued_books"

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    copy_id = Column(Integer,ForeignKey("book_copies.id"),nullable=False)
    issued_date = Column(DateTime,nullable=False)
    return_date =  Column(DateTime,nullable=False)
    actual_return_date = Column(DateTime,nullable=True)
    status = Column(SqlEnum(IssuedBookStatus),nullable=False)

    issued_to = relationship("User",back_populates = "issued_books")
    issued_bookcopy = relationship("BookCopy",back_populates="issued_details")