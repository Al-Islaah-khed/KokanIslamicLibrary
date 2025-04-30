from pydantic import BaseModel

# --- Placeholder Schemas for Related Models ---
# (Replace with actual schemas when defined)
class RoleRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True