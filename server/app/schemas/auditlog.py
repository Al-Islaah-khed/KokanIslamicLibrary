from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class AuditLogRead(BaseModel):
    id: int
    action_by: Optional[int] # User ID or None
    # other fields like action_type, timestamp, details...
    timestamp: datetime # Example field
    action_details: str # Example field

    class Config:
        orm_mode = True
