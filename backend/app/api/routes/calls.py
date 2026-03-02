"""
RepCon Voice Agent - Calls Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, date

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Call

router = APIRouter()


@router.get("/")
async def get_calls(
    institute_id: int = Query(...),
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get calls with filters"""
    query = select(Call).where(Call.institute_id == institute_id)
    
    if status:
        query = query.where(Call.status == status)
    if date_from:
        query = query.where(Call.started_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.where(Call.started_at <= datetime.combine(date_to, datetime.max.time()))
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Paginate
    query = query.offset((page - 1) * limit).limit(limit).order_by(Call.started_at.desc())
    
    result = await db.execute(query)
    calls = result.scalars().all()
    
    return {
        "items": [
            {
                "id": call.id,
                "caller_phone": call.caller_phone,
                "status": call.status,
                "duration": call.duration,
                "started_at": call.started_at.isoformat() if call.started_at else None,
                "answered_at": call.answered_at.isoformat() if call.answered_at else None
            }
            for call in calls
        ],
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/{call_id}")
async def get_call(
    call_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get call details"""
    result = await db.execute(
        select(Call).where(Call.id == call_id)
    )
    call = result.scalar_one_or_none()
    
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found"
        )
    
    return {
        "id": call.id,
        "institute_id": call.institute_id,
        "student_id": call.student_id,
        "caller_phone": call.caller_phone,
        "status": call.status,
        "duration": call.duration,
        "transcript": call.transcript,
        "transcript_language": call.transcript_language,
        "summary": call.summary,
        "outcome": call.outcome,
        "cost": float(call.cost) if call.cost else 0,
        "twilio_call_sid": call.twilio_call_sid,
        "started_at": call.started_at.isoformat() if call.started_at else None,
        "answered_at": call.answered_at.isoformat() if call.answered_at else None,
        "ended_at": call.ended_at.isoformat() if call.ended_at else None
    }


@router.get("/{call_id}/transcript")
async def get_call_transcript(
    call_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get call transcript"""
    result = await db.execute(
        select(Call).where(Call.id == call_id)
    )
    call = result.scalar_one_or_none()
    
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found"
        )
    
    return {
        "call_id": call.id,
        "transcript": call.transcript,
        "language": call.transcript_language,
        "summary": call.summary
    }
