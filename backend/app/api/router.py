from fastapi import APIRouter
from app.api.endpoints import ai_routes, candidates, auth, jobs, applications, admin, insights

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(ai_routes.router, prefix="/ai", tags=["ai"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])

@api_router.get("/")
def read_api_root():
    return {"message": "Welcome to Resume Analyzer API v1", "docs": "/docs"}
