from fastapi import FastAPI,HTTPException,Request
from routes.admin.auth_routes import router as AdminAuthRouter
from routes.admin.user_routes import router as AdminUserRouter
from routes.admin.auditlog_routes import router as AuditLogRouter
from routes.user_auth_routes import router as NonAdminUserAuthRouter
from routes.nonadmin_user_routes import router as NonAdminUserRouter
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import models

app = FastAPI(
    title="Library Management System",
    description="A application which focuses on library management system and more...",
    openapi_tags=[
        {
            "name": "Admin - Auth",
            "description":"Manages the admin authentication"
        },
        {
            "name": "Admin - User",
            "description":"Manages the operations related to the users by the admin, either it is admin user or non admin user, role management as well"
        },
        {
            "name": "Admin - Auditlog",
            "description":"Gives Info about the admin logs auditlogs"
        },
        {
            "name": "User - Auth",
            "description":"Manages the non admin user's authentication with google login, facebook login and verification"
        },
        {
            "name": "User",
            "description":"Manages non admin user related operations like profile update or profile info etc."
        }
    ]
    )

settings = Settings()

origins = [
    settings.CLIENT_BASE_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public",StaticFiles(directory="public"),name="public")

# exception handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=e.status_code,
        content={"message": e.detail}
)

@app.exception_handler(Exception)
def validation_exception(request : Request, err):
    error_message = f"Failed to executed {request.method}: {request.url}"
    return JSONResponse(status_code=400,content = { "message" : f"{error_message}. Detail: {err}"})

# admin routes
app.include_router(AdminAuthRouter)
app.include_router(AdminUserRouter)
app.include_router(AuditLogRouter)

# user routes
app.include_router(NonAdminUserAuthRouter)
app.include_router(NonAdminUserRouter)