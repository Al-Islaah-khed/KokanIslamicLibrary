from repositories.role_repo import RoleRepo
from repositories.user_repo import UserRepo
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import schemas.role as RoleSchema
from enums.Roles import Roles
from helpers.logger import logger

def assign_role_to_user(
    user_id:int,
    role : RoleSchema.AssignRole,
    db: Session,
):
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

    return RoleSchema.AssignResponse(
        message=f"Role '{role.name}' assigned to user '{user.fullname}'"
    )

def remove_role_from_user(
    user_id : int,
    role : RoleSchema.AssignRole,
    db : Session
):
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

    return RoleSchema.AssignResponse(
        message=f"Role '{role.name}' removed from user '{user.fullname}'"
    )