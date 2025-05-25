from repositories.role_repo import RoleRepo
from repositories.user_repo import UserRepo
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import schemas.role as RoleSchema
from enums.Roles import Roles
from helpers.logger import logger
from helpers.protector import is_super_admin
from enums.TargetType import TargetType
import schemas.user as UserSchema
from helpers.password_hash import get_password_hash
from helpers.converters import UserModel_to_AdminSchema,UserModel_to_Schema
from schemas.response import APIResponse
from typing import List,Union,Optional
import traceback

# get all users, filter for admin and non admin users
def get_all_users(db: Session, is_admin: Optional[bool] = None) -> List[Union[UserSchema.Admin, UserSchema.User]]:
    try:
        logger.info(f"[GET_ALL_USERS_START] Fetching all users with is_admin={is_admin}")
        found_users = UserRepo.get_all_users(db=db, is_admin=is_admin)
        logger.info(f"[GET_ALL_USERS_SUCCESS] Found {len(found_users)} users matching is_admin={is_admin}")

        return [
            UserModel_to_AdminSchema(user) if user.is_admin else UserModel_to_Schema(user)
            for user in found_users
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[GET_ALL_USERS_ERROR] Unexpected error during fetching all users: {str(e)}")
        logger.error(f"[GET_ALL_USERS_TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching all users by admin"
        )


# CRUD of admin users
def create_admin(db: Session, user: UserSchema.AdminCreate, create_auditlog):
    try:
        logger.info(f"[CREATE_ADMIN_START] Attempting to create admin with email: '{user.email}'")

        existing_user = UserRepo.get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"[CREATE_ADMIN_FAIL] Email '{user.email}' already registered")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        user.password = get_password_hash(user.password)
        created_user = UserRepo.create_admin_user(db=db, user=user)
        logger.info(f"[CREATE_ADMIN_SUCCESS] Admin '{created_user.email}' created successfully with ID {created_user.id}")

        create_auditlog(
            description=f"Created admin user '{created_user.fullname}' (id={created_user.id})",
            target_id=created_user.id,
            target_type=TargetType.ADMIN
        )

        return UserModel_to_AdminSchema(created_user)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[CREATE_ADMIN_ERROR] Unexpected error during admin creation: {str(e)}")
        logger.error(f"[CREATE_ADMIN_TRACEBACK]\n{traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the admin"
        )

def delete_admin(db: Session, user_id: int, create_auditlog, current_admin: UserSchema.Admin) -> APIResponse:
    try:
        logger.info(f"[DELETE_ADMIN_START] Attempting to delete admin with ID: {user_id}")

        existing_user = UserRepo.get_user_by_id(db=db, user_id=user_id, is_admin=True)
        if not existing_user:
            logger.warning(f"[DELETE_ADMIN_FAIL] Admin with ID {user_id} not found to delete")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found to delete"
            )

        if existing_user.id == current_admin.id:
            logger.warning(f"[DELETE_ADMIN_FAIL] Attempt to delete current logged-in admin ID {current_admin.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete current logged in account"
            )

        if is_super_admin(existing_user):
            logger.warning(f"[DELETE_ADMIN_FAIL] Cannot delete admin with role {Roles.SUPER_ADMIN.value}, user_id={existing_user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete admin with role '{Roles.SUPER_ADMIN.value}'"
            )

        isDeleted = UserRepo.delete_user(db=db, user_id=user_id, is_admin=True)
        if not isDeleted:
            logger.error(f"[DELETE_ADMIN_FAIL] User with ID {user_id} not deleted, unknown error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not deleted, something went wrong"
            )

        logger.info(f"[DELETE_ADMIN_SUCCESS] Admin '{existing_user.fullname}' (ID {existing_user.id}) deleted successfully")

        create_auditlog(
            description=f"Deleted admin user '{existing_user.fullname}' (id={existing_user.id})",
            target_id=existing_user.id,
            target_type=TargetType.ADMIN
        )
        return APIResponse(message="Admin deleted successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[DELETE_ADMIN_ERROR] Unexpected error during admin deletion: {str(e)}")
        logger.error(f"[DELETE_ADMIN_TRACEBACK]\n{traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the admin"
        )


def get_specific_user(db: Session, user_id: int, is_admin: Optional[bool] = None) -> UserSchema.User | UserSchema.Admin:
    try:
        logger.info(f"[GET_SPECIFIC_USER_START] Fetching user with ID: {user_id}, is_admin={is_admin}")
        user = UserRepo.get_user_by_id(db=db, user_id=user_id, is_admin=is_admin)

        if not user:
            logger.warning(f"[GET_SPECIFIC_USER_FAIL] User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found for specified id"
            )

        logger.info(f"[GET_SPECIFIC_USER_SUCCESS] User with ID {user_id} fetched successfully")
        return UserModel_to_AdminSchema(user) if user.is_admin else UserModel_to_Schema(user)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[GET_SPECIFIC_USER_ERROR] Unexpected error while fetching specific user by admin: {str(e)}")
        logger.error(f"[GET_SPECIFIC_USER_TRACEBACK]\n{traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching specific user by admin"
        )

def update_admin(db: Session, user_id: int, user_data: UserSchema.AdminUpdate, create_auditlog) -> UserSchema.Admin:
    try:
        logger.info(f"[UPDATE_ADMIN_START] Attempting to update admin with ID: {user_id}")

        existing_user = UserRepo.get_user_by_id(db=db, user_id=user_id, is_admin=True)
        if not existing_user:
            logger.warning(f"[UPDATE_ADMIN_FAIL] Admin with ID {user_id} not found to update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found to update"
            )

        if is_super_admin(existing_user):
            logger.warning(f"[UPDATE_ADMIN_FAIL] Cannot update admin with role {Roles.SUPER_ADMIN.value}, user_id={existing_user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update admin with role '{Roles.SUPER_ADMIN.value}'"
            )

        if user_data.password:
            logger.info(f"[UPDATE_ADMIN_INFO] Hashing new password for admin ID {user_id}")
            user_data.password = get_password_hash(user_data.password)

        updated_user = UserRepo.update_admin_user(db=db, user_id=user_id, user_data=user_data)

        logger.info(f"[UPDATE_ADMIN_SUCCESS] Admin '{updated_user.fullname}' (ID {updated_user.id}) updated successfully")

        create_auditlog(
            description=f"Updated admin user '{updated_user.fullname}' (id={updated_user.id})",
            target_id=updated_user.id,
            target_type=TargetType.ADMIN
        )
        return UserModel_to_AdminSchema(updated_user)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[UPDATE_ADMIN_ERROR] Unexpected error during admin update: {str(e)}")
        logger.error(f"[UPDATE_ADMIN_TRACEBACK]\n{traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating admin user"
        )

# Role related user functions
def assign_role_to_user(
    user_id: int,
    role: RoleSchema.AssignRole,
    db: Session,
    create_auditlog
) -> RoleSchema.AssignResponse:
    try:
        logger.info(f"[ASSIGN_ROLE_START] Attempting to assign role_id={role.role_id} to user_id={user_id}")

        user = UserRepo.get_user_by_id(db=db, user_id=user_id)
        if not user:
            logger.warning(f"[ASSIGN_ROLE_FAIL] User with id={user_id} not found")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        if is_super_admin(user):
            logger.warning(f"[ASSIGN_ROLE_FAIL] Cannot assign role to SUPER_ADMIN user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot assign roles on the '{Roles.SUPER_ADMIN.value}' as it has full access to admin panel"
            )

        role_obj = RoleRepo.get_role_by_id(db=db, role_id=role.role_id)
        if not role_obj:
            logger.warning(f"[ASSIGN_ROLE_FAIL] Role with id={role.role_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        if role_obj.name == Roles.SUPER_ADMIN.value:
            logger.warning(f"[ASSIGN_ROLE_FAIL] Attempt to assign SUPER_ADMIN role to user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only one admin can have '{Roles.SUPER_ADMIN.value}' role"
            )

        if role_obj in user.roles:
            logger.warning(f"[ASSIGN_ROLE_FAIL] User id={user_id} already has role '{role_obj.name}'")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has this role")

        UserRepo.assign_role(db=db, user=user, role=role_obj)
        logger.info(f"[ASSIGN_ROLE_SUCCESS] Assigned role '{role_obj.name}' to user '{user.fullname}' (id={user_id})")

        create_auditlog(
            description=f"Assigned role '{role_obj.name}' to user '{user.fullname}' (id={user_id})",
            target_id=user_id,
            target_type=(TargetType.ADMIN if user.is_admin else TargetType.CLIENT)
        )

        return RoleSchema.AssignResponse(
            message=f"Role '{role_obj.name}' assigned to user '{user.fullname}'"
        )

    except HTTPException:
        logger.warning(f"[ASSIGN_ROLE_HTTP_EXCEPTION] HTTPException while assigning role_id={role.role_id} to user_id={user_id}, re-raising")
        raise
    except Exception as e:
        logger.error(f"[ASSIGN_ROLE_ERROR] Unexpected error while assigning role: {str(e)}")
        logger.error(f"[ASSIGN_ROLE_TRACEBACK]\n{traceback.format_exc()}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


def remove_role_from_user(
    user_id: int,
    role: RoleSchema.AssignRole,
    db: Session,
    create_auditlog
) -> RoleSchema.AssignResponse:
    try:
        logger.info(f"[REMOVE_ROLE_START] Attempting to remove role_id={role.role_id} from user_id={user_id}")

        user = UserRepo.get_user_by_id(db=db, user_id=user_id)
        if not user:
            logger.warning(f"[REMOVE_ROLE_FAIL] User with id={user_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if is_super_admin(user):
            logger.warning(f"[REMOVE_ROLE_FAIL] Attempt to remove roles from SUPER_ADMIN user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot remove roles from '{Roles.SUPER_ADMIN.value}'"
            )

        role_obj = RoleRepo.get_role_by_id(db=db, role_id=role.role_id)
        if not role_obj:
            logger.warning(f"[REMOVE_ROLE_FAIL] Role with id={role.role_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        if role_obj.name == Roles.SUPER_ADMIN.value:
            logger.warning(f"[REMOVE_ROLE_FAIL] Attempt to remove SUPER_ADMIN role")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot remove '{Roles.SUPER_ADMIN.value}' role"
            )

        if role_obj not in user.roles:
            logger.warning(f"[REMOVE_ROLE_FAIL] User id={user_id} does not have role '{role_obj.name}'")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't have this role")

        UserRepo.remove_role(db=db, user=user, role=role_obj)
        logger.info(f"[REMOVE_ROLE_SUCCESS] Removed role '{role_obj.name}' from user '{user.fullname}' (id={user_id})")

        create_auditlog(
            description=f"Removed role '{role_obj.name}' from user '{user.fullname}' (id={user_id})",
            target_id=user_id,
            target_type=(TargetType.ADMIN if user.is_admin else TargetType.CLIENT)
        )

        return RoleSchema.AssignResponse(
            message=f"Removed role '{role_obj.name}' from user '{user.fullname}' (id={user_id})"
        )

    except HTTPException:
        logger.warning(f"[REMOVE_ROLE_HTTP_EXCEPTION] HTTPException while removing role_id={role.role_id} from user_id={user_id}, re-raising")
        raise
    except Exception as e:
        logger.error(f"[REMOVE_ROLE_ERROR] Unexpected error while removing role: {str(e)}")
        logger.error(f"[REMOVE_ROLE_TRACEBACK]\n{traceback.format_exc()}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")