from repositories.role_repo import RoleRepo
from repositories.user_repo import UserRepo
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import schemas.role as RoleSchema
from enums.Roles import Roles
from helpers.logger import logger
from enums.TargetType import TargetType
import schemas.user as UserSchema
from helpers.password_hash import get_password_hash
from helpers.converters import UserModel_to_AdminSchema
from schemas.response import APIResponse
from typing import List

# CRUD of admin users
def create_admin(db: Session, user: UserSchema.AdminCreate,create_auditlog):
    try:
        existing_user = UserRepo.get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"Admin creation failed: email '{user.email}' already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user.password = get_password_hash(user.password)
        created_user = UserRepo.create_admin_user(db=db, user=user)
        logger.info(f"Admin '{created_user.email}' created successfully with ID {created_user.id}")

        create_auditlog(
            description=f"Created admin user '{created_user.fullname}' (id={created_user.id})",
            target_id=created_user.id,
            target_type=TargetType.ADMIN
        )

        return UserModel_to_AdminSchema(created_user)

    except HTTPException:
        raise  # Let FastAPI handle it
    except Exception as e:
        logger.error(f"Unexpected error during admin creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the admin"
        )

def delete_admin(db: Session, user_id: int,create_auditlog,current_admin : UserSchema.Admin) -> APIResponse:
    try:
        existing_user = UserRepo.get_admin_user_by_id(db=db, user_id=user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found to delete"
            )

        if existing_user.id == current_admin.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete current logged in account"
            )

        if Roles.SUPER_ADMIN.value in [role.name for role in existing_user.roles]:
            logger.warning(
                f"Cannot delete admin with role {Roles.SUPER_ADMIN.value}, user_id={existing_user.id}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete admin with role '{Roles.SUPER_ADMIN.value}'"
            )

        isDeleted = UserRepo.delete_user(db=db, user_id=user_id)
        if not isDeleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not deleted, something went wrong"
            )

        logger.info(f"Admin '{existing_user.fullname}' deleted successfully")

        create_auditlog(
            description=f"Deleted admin user '{existing_user.fullname}' (id={existing_user.id})",
            target_id=existing_user.id,
            target_type=TargetType.ADMIN
        )
        return APIResponse(message="Admin deleted successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during admin deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the admin"
        )

def get_all_admins(db : Session) -> List[UserSchema.Admin]:
    try:
        admin_users = UserRepo.get_all_admin_users(db)
        return [UserModel_to_AdminSchema(admin) for admin in admin_users]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching all admin users"
        )

def get_specific_admin(db:Session,user_id : int) -> UserSchema.Admin:
    try:
        admin_user = UserRepo.get_admin_user_by_id(db=db,user_id=user_id)

        if not admin_user:
            raise HTTPException(
                status=status.HTTP_404_NOT_FOUND,
                details="Admin not found for specified id"
            )

        return UserModel_to_AdminSchema(admin_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching all admin users"
        )


def update_admin(db:Session,user_id: int,user_data: UserSchema.AdminUpdate,create_auditlog) -> UserSchema.Admin:
    try:
        existing_user = UserRepo.get_user_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found to update"
            )

        if Roles.SUPER_ADMIN.value in [role.name for role in existing_user.roles]:
            logger.warning(
                f"Cannot update admin with role {Roles.SUPER_ADMIN.value}, user_id={existing_user.id}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update admin with role '{Roles.SUPER_ADMIN.value}'"
            )

        if user_data.password:
            user_data.password = get_password_hash(user_data.password)

        updated_user = UserRepo.update_admin_user(db=db,user_id=user_id,user_data=user_data)

        create_auditlog(
            description=f"Updated admin user '{updated_user.fullname}' (id={updated_user.id})",
            target_id=updated_user.id,
            target_type=TargetType.ADMIN
        )
        return UserModel_to_AdminSchema(updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating admin user"
        )

# Role related user functions

def assign_role_to_user(
    user_id:int,
    role : RoleSchema.AssignRole,
    db: Session,
    create_auditlog
) -> RoleSchema.AssignResponse:
    logger.info(f"Attempting to assign role_id={role.role_id} to user_id={user_id}")

    user = UserRepo.get_user_by_id(db=db,user_id=user_id)

    if not user:
        logger.warning(f"User with id={user_id} not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if Roles.SUPER_ADMIN.value in [role.name for role in user.roles]:
        logger.warning(f"Cannot assign role to SUPER_ADMIN user_id={user_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot assign roles on the '{Roles.SUPER_ADMIN.value}' as it have full access to admin panel")

    role = RoleRepo.get_role_by_id(db=db,role_id=role.role_id)

    if not role:
        logger.warning(f"Role with id={role.role_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if role.name == Roles.SUPER_ADMIN.value:
        logger.warning("Attempt to assign SUPER_ADMIN role")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Only one admin can have '{Roles.SUPER_ADMIN.value}' role")

    if role in user.roles:
        logger.warning(f"User id={user_id} already has role '{role.name}'")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has this role")

    UserRepo.assign_role(db=db,user=user,role=role)
    logger.info(f"Assigned role '{role.name}' to user '{user.fullname}' (id={user_id})")

    # logging in the database
    create_auditlog(
        description=f"Assigned role '{role.name}' to user '{user.fullname}' (id={user_id})",
        target_id=user_id,
        target_type=(TargetType.ADMIN if user.is_admin else TargetType.CLIENT)
    )


    return RoleSchema.AssignResponse(
        message=f"Role '{role.name}' assigned to user '{user.fullname}'"
    )

def remove_role_from_user(
    user_id : int,
    role : RoleSchema.AssignRole,
    db : Session,
    create_auditlog
) -> RoleSchema.AssignResponse:
    logger.info(f"Attempting to remove role_id={role.role_id} from user_id={user_id}")

    user = UserRepo.get_user_by_id(db=db,user_id=user_id)
    if not user:
        logger.warning(f"User with id={user_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if Roles.SUPER_ADMIN.value in [role.name for role in user.roles]:
        logger.warning(f"Attempt to remove roles from SUPER_ADMIN user_id={user_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot remove roles from '{Roles.SUPER_ADMIN.value}'")

    role = RoleRepo.get_role_by_id(db=db,role_id=role.role_id)

    if not role:
        logger.warning(f"Role with id={role.role_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if not role in user.roles:
        logger.warning(f"User id={user_id} does not have role '{role.name}'")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't has this role")

    if role.name == Roles.SUPER_ADMIN.value:
        logger.warning("Attempt to remove SUPER_ADMIN role")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Cannot remove '{Roles.SUPER_ADMIN.value}' role")

    UserRepo.remove_role(db=db,user=user,role=role)
    logger.info(f"Removed role '{role.name}' from user '{user.fullname}' (id={user_id})")

    # logging in the database
    create_auditlog(
        description=f"Removed role '{role.name}' from user '{user.fullname}' (id={user_id})",
        target_id=user_id,
        target_type=(TargetType.ADMIN if user.is_admin else TargetType.CLIENT)
    )

    return RoleSchema.AssignResponse(
        message=f"Removed role '{role.name}' from user '{user.fullname}' (id={user_id})"
    )