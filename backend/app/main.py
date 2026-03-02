"""
RepCon Voice Agent - Main FastAPI Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.session import init_db
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting up RepCon Voice Agent...")
    await init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down RepCon Voice Agent...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Voice Receptionist for Educational Institutes",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": str(request.url)
        }
    )


# Include API router
app.include_router(api_router, prefix="/api/v1")


# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "service": "RepCon Voice Agent"}


@app.get("/ready")
async def readiness_check():
    """Readiness check"""
    return {"status": "ready", "version": settings.APP_VERSION}


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }
