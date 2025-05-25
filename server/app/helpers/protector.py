from enums.Roles import Roles
from models.user import User

def is_super_admin(user: User) -> bool:
    return any(role.name == Roles.SUPER_ADMIN.value for role in user.roles)