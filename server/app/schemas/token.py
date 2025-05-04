from pydantic import BaseModel,EmailStr
from typing import List

class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    is_active: bool
    roles: List[str] = []