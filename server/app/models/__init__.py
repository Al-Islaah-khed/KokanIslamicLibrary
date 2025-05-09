from db.database import Base

from .role import Role
from .permission import Permission
from .auditlog import AuditLog
from .digitalaccess import DigitalAccess
from .book import Book
from .issuedbook import IssuedBook
from .bookcopy import BookCopy
from .bookupload_request import BookUploadRequest
from .category import Category
from .subcategory import SubCategory
from .location import Location
from .booklocation import BookLocation
from .language import Language