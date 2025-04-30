
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PermissionRead(BaseModel):
    id: int
    permission_type: str
    granted: bool
    granted_to: int # User ID
    granted_by: Optional[int] # User ID or None
    granted_at: datetime

    class Config:
        orm_mode = True
