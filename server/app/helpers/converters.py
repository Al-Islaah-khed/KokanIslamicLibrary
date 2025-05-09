from models.auditlog import AuditLog
from models.user import User
import schemas.auditlog as AuditLogSchema
import schemas.user as UserSchema

def UserModel_to_Schema(db_user : User) -> UserSchema.User :
    # user_data = user.__dict__
    # role_names = [role.name for role in user.roles]
    # user_data["roles"] = role_names
    # return UserSchema.User(**user_data)
    return UserSchema.User.model_validate(db_user)

def UserModel_to_AdminSchema(db_user : User) -> UserSchema.Admin :
    # user_data = user.__dict__
    # role_names = [role.name for role in user.roles]
    # user_data["roles"] = role_names
    # return UserSchema.User(**user_data)
    return UserSchema.Admin.model_validate(db_user)

def AuditLogModel_to_Schema(db_auditlog : AuditLog) -> AuditLogSchema.AuditLog:
    # log_data = log.__dict__

    # # getting the user data in dictionary
    # user_data = log.user.__dict__
    # role_names = [role.name for role in log.user.roles]
    # user_data['roles'] = role_names

    # log_data['user'] = user_data
    # return AuditLogSchema.AuditLog(**log_data)
    return AuditLogSchema.AuditLog.model_validate(db_auditlog)