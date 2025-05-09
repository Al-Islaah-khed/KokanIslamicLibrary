from pydantic import BaseModel, EmailStr,Field,ConfigDict
from typing import List, Optional,Literal
from .permission import PermissionRead
from .role import Role


# normal users schema
class UserBase(BaseModel):
    fullname: str = Field(..., min_length=3,max_length=100)
    email: EmailStr = Field(..., min_length=5,max_length=100)
    is_admin: bool = False
    is_active: bool = True

class User(UserBase):
    id : int
    roles : Optional[List[Role]] = []

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")

class UserUpdate(BaseModel):
    fullname: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, description="New password (leave blank to keep current)")
    is_active: Optional[bool] = None

class UserLoginResponse(BaseModel):
    token: str
    user: User

# admin users schema
class AdminBase(BaseModel):
    fullname: str = Field(..., min_length=3,max_length=100)
    email: EmailStr = Field(..., min_length=5,max_length=100)
    is_admin: bool = False
    is_active: bool = True

class Admin(AdminBase):
    id : int
    roles : Optional[List[Role]] = []

    model_config = ConfigDict(from_attributes=True)

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=8, description="User password")
    is_admin : Literal[True] = True

class AdminUpdate(BaseModel):
    fullname: Optional[str] = Field(None, max_length=100)
    # email: Optional[EmailStr] = Field(None, max_length=100) # email should not be updated
    password: Optional[str] = Field(None, min_length=8, description="New password (leave blank to keep current)")
    # is_admin: Optional[bool] = None # is admin field should not be updated
    is_active: Optional[bool] = None

class AdminLogin(BaseModel):
    email : str = Field(...,min_length=3,description="Email of the user")
    password : str = Field(...,min_length=8,description="Password of the user")

class GetAllAdminRouteResponse(BaseModel):
    admins : List[Admin]

class AdminLoginResponse(BaseModel):
    token: str
    user: Admin