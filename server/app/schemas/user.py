from pydantic import BaseModel, EmailStr,Field
from typing import List, Optional
from .permission import PermissionRead
from .role import RoleRead

class UserBase(BaseModel):
    fullname: str = Field(..., min_length=3,max_length=100)
    email: EmailStr = Field(..., min_length=5,max_length=100)
    is_admin: bool = False
    is_active: bool = True

class User(UserBase):
    id : int
    roles : Optional[List[str]] = []

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")

class UserUpdate(BaseModel):
    fullname: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, description="New password (leave blank to keep current)")
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    # Optional: Add role IDs if roles can be updated
    role_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : str = Field(...,min_length=3,description="Email of the user")
    password : str = Field(...,min_length=8,description="Password of the user")

class UserLoginResponse(BaseModel):
    token: str
    user: User

# Schema for reading user data with relationships (output)
# Be mindful of circular dependencies and payload size
class UserReadWithRoles(User):
    roles: List[RoleRead] = []

class UserReadWithDetails(UserReadWithRoles):
    permissions_granted_to: List[PermissionRead] = []
    # permissions_granted_by: List[PermissionRead] = [] # Might be too much data usually
    # digital_access: List[DigitalAccessRead] = [] # Might be too much data usually
    # submitted_uploads: List[BookUploadRequestReadBasic] = [] # Usually fetched separately
    # reviewed_uploads: List[BookUploadRequestReadBasic] = [] # Usually fetched separately
    # added_book_copies: List[BookCopyReadBasic] = [] # Usually fetched separately
    # action_performed: List[AuditLogRead] = [] # Usually fetched separately via audit endpoint

    # Add other relationships as needed, but be selective