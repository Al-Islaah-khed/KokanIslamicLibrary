
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BookCopyReadBasic(BaseModel): # Basic info, avoid deep nesting
    id: int
    book_id: int
    status: str # Use the actual enum if available

    class Config:
        orm_mode = True