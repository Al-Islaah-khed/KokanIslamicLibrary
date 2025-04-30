from fastapi import FastAPI
from routes.auth_routes import router as AdminAuthRouter
from db.database import create_tables

from models.role import Role
from models.permission import Permission
from models.auditlog import AuditLog
from models.digitalaccess import DigitalAccess
from models.book import Book
from models.issuedbook import IssuedBook
from models.bookcopy import BookCopy
from models.bookupload_request import BookUploadRequest
from models.category import Category
from models.subcategory import SubCategory
from models.location import Location
from models.booklocation import BookLocation
from models.language import Language

app = FastAPI(title="Library Management System")

create_tables()

app.include_router(AdminAuthRouter,prefix="/auth/admin")