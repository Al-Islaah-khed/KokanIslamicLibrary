from fastapi import FastAPI
from routes.admin.auth_routes import router as AdminAuthRouter
from routes.admin.user_routes import router as AdminUserRouter

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

# admin routes
app.include_router(AdminAuthRouter)
app.include_router(AdminUserRouter)