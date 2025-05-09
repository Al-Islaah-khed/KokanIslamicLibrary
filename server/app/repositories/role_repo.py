from models.role import Role
from sqlalchemy.orm import Session
from typing import List,Optional

class RoleRepo():

    def get_role_by_id(db : Session,role_id : int) -> Optional[Role]:
        return db.query(Role).filter(Role.id == role_id).first()

    def get_all_roles(db : Session) -> List[Role]:
        return db.query(Role).all()