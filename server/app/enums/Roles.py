from enum import Enum

class Roles(Enum):
    SUPER_ADMIN = "super_admin"
    LIBRARIAN = "librarian"
    STAFF_ADMIN = "staff_admin"
    AUDITOR = "auditor"