from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class BookUploadRequestReadBasic(BaseModel): # Basic info
    id: int
    book_id: Optional[int]
    status: str # Use the actual enum if available
    submitted_at: datetime

    class Config:
        orm_mode = True
