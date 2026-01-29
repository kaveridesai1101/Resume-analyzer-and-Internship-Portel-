from fastapi import APIRouter
from app.api.endpoints import ai_routes, students, auth, internships, applications, admin, insights, recruiters

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(ai_routes.router, prefix="/ai", tags=["ai"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(internships.router, prefix="/internships", tags=["internships"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(recruiters.router, prefix="/recruiters", tags=["recruiters"])

@api_router.get("/")
def read_api_root():
    return {"message": "Welcome to Resume Analyzer API v1", "docs": "/docs"}
