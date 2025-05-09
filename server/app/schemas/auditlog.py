from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from enums.TargetType import TargetType
import schemas.user as UserSchema
class AuditLogBase(BaseModel):
    action_by: int
    target_id: Optional[int] = None
    target_type: Optional[TargetType] = None
    description: str = Field(..., min_length=5)
    ip_address: str = Field(..., min_length=7)  # e.g., "127.0.0.1"
    user_agent: str = Field(..., min_length=3)

    model_config = ConfigDict(from_attributes=True)

class AuditLogCreate(AuditLogBase):
    pass  # All required fields already in base

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime
    user: Optional[UserSchema.Admin] = None

    model_config = ConfigDict(from_attributes=True)

