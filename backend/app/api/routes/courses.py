"""
RepCon Voice Agent - Courses Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Course

router = APIRouter()


@router.get("/")
async def get_courses(
    institute_id: int = Query(...),
    mode: Optional[str] = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get courses"""
    query = select(Course).where(Course.institute_id == institute_id)
    
    if mode:
        query = query.where(Course.mode == mode)
    if active_only:
        query = query.where(Course.is_active == True)
    
    result = await db.execute(query.order_by(Course.display_order, Course.course_name))
    courses = result.scalars().all()
    
    return {
        "items": [
            {
                "id": course.id,
                "course_name": course.course_name,
                "course_code": course.course_code,
                "description": course.description,
                "duration": course.duration,
                "fee": float(course.fee),
                "fee_currency": course.fee_currency,
                "job_roles": course.job_roles or [],
                "mode": course.mode,
                "is_active": course.is_active
            }
            for course in courses
        ],
        "total": len(courses)
    }


@router.get("/{course_id}")
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get course by ID"""
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return {
        "id": course.id,
        "institute_id": course.institute_id,
        "course_name": course.course_name,
        "course_code": course.course_code,
        "description": course.description,
        "duration": course.duration,
        "duration_days": course.duration_days,
        "fee": float(course.fee),
        "fee_currency": course.fee_currency,
        "job_roles": course.job_roles or [],
        "syllabus": course.syllabus,
        "prerequisites": course.prerequisites,
        "eligibility": course.eligibility,
        "mode": course.mode,
        "start_date": course.start_date.isoformat() if course.start_date else None,
        "batch_time": course.batch_time,
        "certificate": course.certificate,
        "placement_assistance": course.placement_assistance,
        "is_active": course.is_active
    }


@router.post("/sync")
async def sync_courses(
    institute_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Trigger Google Sheets sync"""
    # This would normally call the Google Sheets sync service
    # For now, return a placeholder
    return {
        "message": "Course sync initiated",
        "institute_id": institute_id,
        "status": "processing"
    }
