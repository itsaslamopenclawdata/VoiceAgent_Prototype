"""
RepCon Voice Agent - Leads Routes
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from datetime import datetime, date

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Student, Institute

router = APIRouter()


@router.get("/")
async def get_leads(
    institute_id: int = Query(...),
    status: Optional[str] = None,
    course_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get leads with filters"""
    # Build query
    query = select(Student).where(Student.institute_id == institute_id)
    
    # Apply filters
    if status:
        query = query.where(Student.status == status)
    if course_id:
        query = query.where(Student.course_interest == course_id)
    if date_from:
        query = query.where(Student.created_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.where(Student.created_at <= datetime.combine(date_to, datetime.max.time()))
    if search:
        query = query.where(
            or_(
                Student.name.ilike(f"%{search}%"),
                Student.phone.ilike(f"%{search}%"),
                Student.email.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit).order_by(Student.created_at.desc())
    
    # Execute
    result = await db.execute(query)
    leads = result.scalars().all()
    
    return {
        "items": [
            {
                "id": lead.id,
                "name": lead.name,
                "phone": lead.phone,
                "email": lead.email,
                "course_interest": lead.course_interest,
                "status": lead.status,
                "source": lead.source,
                "created_at": lead.created_at.isoformat() if lead.created_at else None
            }
            for lead in leads
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{lead_id}")
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get lead by ID"""
    result = await db.execute(
        select(Student).where(Student.id == lead_id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    return {
        "id": lead.id,
        "institute_id": lead.institute_id,
        "name": lead.name,
        "phone": lead.phone,
        "email": lead.email,
        "course_interest": lead.course_interest,
        "status": lead.status,
        "priority": lead.priority,
        "notes": lead.notes,
        "source": lead.source,
        "created_at": lead.created_at.isoformat() if lead.created_at else None,
        "updated_at": lead.updated_at.isoformat() if lead.updated_at else None
    }


@router.post("/")
async def create_lead(
    name: str,
    phone: str,
    institute_id: int,
    email: Optional[str] = None,
    course_interest: Optional[int] = None,
    source: str = "voice_agent",
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new lead"""
    # Check for duplicate phone
    result = await db.execute(
        select(Student).where(
            Student.phone == phone,
            Student.institute_id == institute_id
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing lead
        existing.name = name
        existing.email = email or existing.email
        existing.course_interest = course_interest or existing.course_interest
        existing.last_contacted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return {
            "id": existing.id,
            "message": "Lead updated (duplicate phone)"
        }
    
    # Create new lead
    lead = Student(
        name=name,
        phone=phone,
        email=email,
        institute_id=institute_id,
        course_interest=course_interest,
        source=source,
        status="new"
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    
    return {
        "id": lead.id,
        "message": "Lead created successfully"
    }


@router.put("/{lead_id}")
async def update_lead(
    lead_id: int,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update lead"""
    result = await db.execute(
        select(Student).where(Student.id == lead_id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    if status:
        lead.status = status
        if status == "enrolled":
            lead.converted_at = datetime.utcnow()
    if notes is not None:
        lead.notes = notes
    if priority:
        lead.priority = priority
    if assigned_to:
        lead.assigned_to = assigned_to
    
    lead.last_contacted_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(lead)
    
    return {
        "id": lead.id,
        "status": lead.status,
        "message": "Lead updated successfully"
    }


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete lead"""
    result = await db.execute(
        select(Student).where(Student.id == lead_id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    await db.delete(lead)
    await db.commit()
    
    return {"message": "Lead deleted successfully"}


@router.get("/export/csv")
async def export_leads_csv(
    institute_id: int = Query(...),
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Export leads to CSV"""
    # Build query (same as get_leads)
    query = select(Student).where(Student.institute_id == institute_id)
    
    if status:
        query = query.where(Student.status == status)
    if date_from:
        query = query.where(Student.created_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.where(Student.created_at <= datetime.combine(date_to, datetime.max.time()))
    
    result = await db.execute(query.order_by(Student.created_at.desc()))
    leads = result.scalars().all()
    
    # Generate CSV
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Phone", "Email", "Status", "Source", "Created At"])
    
    for lead in leads:
        writer.writerow([
            lead.id,
            lead.name,
            lead.phone,
            lead.email or "",
            lead.status,
            lead.source,
            lead.created_at.isoformat() if lead.created_at else ""
        ])
    
    return {
        "filename": f"leads_{institute_id}_{date.today()}.csv",
        "content": output.getvalue()
    }
