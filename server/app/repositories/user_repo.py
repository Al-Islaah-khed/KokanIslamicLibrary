from models.user import User
from typing import Optional,List
from sqlalchemy.orm import Session
import schemas.user as UserSchema
from models.role import Role
from datetime import datetime
class UserRepo():

    # user and admin both can find by these methods
    def update_last_login(db : Session,user : User) -> User:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_id(db : Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_all_users(db : Session) -> List[User]:
        return db.query(User).all()

    def get_user_by_email(db : Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def delete_user(db:Session,user_id : int) -> bool:
        result = db.query(User).filter(User.id == user_id).delete()
        db.commit()
        return result > 0

    # only non admin users repository methods
    def create_nonadmin_user(db:Session , user : UserSchema.UserCreate) -> User:
        new_user = User(
            fullname = user.fullname,
            email=user.email,
            profile_image=user.profile_image,
            auth_provider = user.auth_provider,
            provider_id = user.provider_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_all_nonadmin_users(db:Session)-> List[User]:
        return db.query(User).filter(User.is_admin == False).all()


    # only admin users repository methods
    def get_admin_user_by_id(db: Session,user_id : int)-> Optional[User]:
        return db.query(User).filter(User.id == user_id,User.is_admin == True).first()

    def get_admin_user_by_email(db : Session, email: str) -> Optional[User]:
            return db.query(User).filter(User.email == email,User.is_admin == True).first()

    def get_all_admin_users(db:Session) -> List[User]:
        return db.query(User).filter(User.is_admin == True).all()

    def create_admin_user(db : Session, user: UserSchema.AdminCreate ) -> User:
        new_user = User(
            fullname=user.fullname,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin,
            is_active=True,
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update_admin_user(db: Session, user_id:int, user_data: UserSchema.AdminUpdate) -> User:

        update_data = {}

        if user_data.fullname is not None:
            update_data['fullname'] = user_data.fullname
        if user_data.password is not None:
            update_data['password'] = user_data.password
        if user_data.is_active is not None:
            update_data['is_active'] = user_data.is_active

        db.query(User).filter(User.id == user_id).update(update_data)
        db.commit()

        updated_user = db.query(User).filter(User.id == user_id).first()
        return updated_user

# user's role related methods
    def assign_role(db: Session,user: User,role: Role) -> User:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
        return user

    def remove_role(db:Session,user: User,role : Role) -> User:
        user.roles.remove(role)
        db.commit()
        db.refresh(user)
        return user