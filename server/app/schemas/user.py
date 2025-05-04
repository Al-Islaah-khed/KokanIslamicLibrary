from pydantic import BaseModel, EmailStr,Field,ConfigDict
from typing import List, Optional
from .permission import PermissionRead

class UserBase(BaseModel):
    fullname: str = Field(..., min_length=3,max_length=100)
    email: EmailStr = Field(..., min_length=5,max_length=100)
    is_admin: bool = False
    is_active: bool = True

class User(UserBase):
    id : int
    roles : Optional[List[str]] = []

    model_config = ConfigDict(from_attributes=True)


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

class UserLogin(BaseModel):
    email : str = Field(...,min_length=3,description="Email of the user")
    password : str = Field(...,min_length=8,description="Password of the user")

class UserLoginResponse(BaseModel):
    token: str
    user: User