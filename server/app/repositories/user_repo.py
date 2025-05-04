from models.user import User
from typing import Optional
from sqlalchemy.orm import Session
import schemas.user as UserSchema
from models.role import Role
class UserRepo():

    def get_user_by_id(db : Session, user_id: int) -> Optional[UserSchema.User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(db : Session, email: str) -> Optional[UserSchema.User]:
        return db.query(User).filter(User.email == email).first()

    def get_all_users(db : Session):
        return db.query(User).all()

    def create_user(db : Session, user: UserSchema.UserCreate ):
        new_user = User(
            fullname=user.fullname,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin,
            is_active=True
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def assign_role(db: Session,user: User,role: Role):
        user.roles.append(role)
        db.commit()
        db.refresh(user)
        return user

    def remove_role(db:Session,user: User,role : Role):
        user.roles.remove(role)
        db.commit()
        db.refresh(user)
        return user