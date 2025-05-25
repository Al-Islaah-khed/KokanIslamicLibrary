from fastapi import FastAPI,HTTPException,Request
from routes.admin.auth_routes import router as AdminAuthRouter
from routes.admin.user_routes import router as AdminUserRouter
from routes.admin.auditlog_routes import router as AuditLogRouter
from routes.user_auth_routes import router as NonAdminUserAuthRouter
from routes.nonadmin_user_routes import router as NonAdminUserRouter
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from fastapi.responses import JSONResponse


import models

app = FastAPI(title="Library Management System")

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