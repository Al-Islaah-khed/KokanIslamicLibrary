from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str
    description : str

class Role(RoleBase):
    id : int

class AssignRole(BaseModel):
    role_id: int

class AssignResponse(BaseModel):
    message : str

class CreateRole(RoleBase):
    pass