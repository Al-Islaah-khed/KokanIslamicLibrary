from fastapi import FastAPI
from routes.admin.auth_routes import router as AdminAuthRouter
from routes.admin.user_routes import router as AdminUserRouter
from routes.admin.auditlog_routes import router as AuditLogRouter

import models

app = FastAPI(title="Library Management System")

# admin routes
app.include_router(AdminAuthRouter)
app.include_router(AdminUserRouter)
app.include_router(AuditLogRouter)