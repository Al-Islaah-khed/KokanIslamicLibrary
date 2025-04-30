from pydantic import BaseModel,EmailStr
from typing import Optional,List

class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    is_admin: Optional[bool] = False
    is_active: bool = True
    roles: Optional[List[str]] = []