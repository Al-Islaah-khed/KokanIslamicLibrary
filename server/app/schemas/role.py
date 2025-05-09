from pydantic import BaseModel,ConfigDict

class RoleBase(BaseModel):
    name: str
    description : str

class Role(RoleBase):
    id : int

    model_config = ConfigDict(from_attributes=True)

class AssignRole(BaseModel):
    role_id: int

class AssignResponse(BaseModel):
    message : str

class CreateRole(RoleBase):
    pass