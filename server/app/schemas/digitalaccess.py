
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class DigitalAccessRead(BaseModel):
    id: int
    book_id: int # Assuming book relation exists
    access_granted: bool
    granted_at: datetime # Assuming timestamp exists

    class Config:
        orm_mode = True