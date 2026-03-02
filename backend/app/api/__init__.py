"""
RepCon Voice Agent - API Routes
"""
from fastapi import APIRouter

from app.api.routes import auth, leads, calls, courses, stats, settings, webhooks

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads"])
api_router.include_router(calls.router, prefix="/calls", tags=["Calls"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(stats.router, prefix="/stats", tags=["Statistics"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
