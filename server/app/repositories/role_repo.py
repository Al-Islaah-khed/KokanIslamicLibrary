from models.role import Role
from sqlalchemy.orm import Session

class RoleRepo():

    def get_role_by_id(db : Session,role_id : int):
        return db.query(Role).filter(Role.id == role_id).first()

    def get_all_roles(db : Session):
        return db.query(Role).all()