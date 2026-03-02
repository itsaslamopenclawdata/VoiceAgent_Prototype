"""
RepCon Voice Agent - Statistics Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Student, Call, DailyStats

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    institute_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get dashboard statistics"""
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Today's calls
    today_start = datetime.combine(today, datetime.min.time())
    calls_today_result = await db.execute(
        select(func.count(Call.id)).where(
            Call.institute_id == institute_id,
            Call.started_at >= today_start
        )
    )
    calls_today = calls_today_result.scalar()
    
    # Today's leads
    leads_today_result = await db.execute(
        select(func.count(Student.id)).where(
            Student.institute_id == institute_id,
            Student.created_at >= today_start
        )
    )
    leads_today = leads_today_result.scalar()
    
    # This week's leads
    week_start = datetime.combine(week_ago, datetime.min.time())
    leads_week_result = await db.execute(
        select(func.count(Student.id)).where(
            Student.institute_id == institute_id,
            Student.created_at >= week_start
        )
    )
    leads_week = leads_week_result.scalar()
    
    # Conversion rate (enrolled / total)
    enrolled_result = await db.execute(
        select(func.count(Student.id)).where(
            Student.institute_id == institute_id,
            Student.status == "enrolled"
        )
    )
    enrolled = enrolled_result.scalar()
    
    total_result = await db.execute(
        select(func.count(Student.id)).where(
            Student.in_id
        )
stitute_id == institute    )
    total = total_result.scalar()
    
    conversion_rate = (enrolled / total * 100) if total > 0 else 0
    
    return {
        "today": {
            "calls": calls_today,
            "leads": leads_today
        },
        "this_week": {
            "leads": leads_week
        },
        "conversion_rate": round(conversion_rate, 1),
        "total_leads": total,
        "enrolled": enrolled
    }


@router.get("/analytics")
async def get_analytics(
    institute_id: int = Query(...),
    days: int = Query(30, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics data"""
    # Get daily stats
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    result = await db.execute(
        select(DailyStats).where(
            DailyStats.institute_id == institute_id,
            DailyStats.date >= start_date
        ).order_by(DailyStats.date)
    )
    stats = result.scalars().all()
    
    # Format for chart
    chart_data = [
        {
            "date": stat.date.isoformat(),
            "total_calls": stat.total_calls,
            "answered_calls": stat.answered_calls,
            "missed_calls": stat.missed_calls,
            "new_leads": stat.new_leads,
            "converted_leads": stat.converted_leads
        }
        for stat in stats
    ]
    
    # Summary
    total_calls = sum(s.total_calls for s in stats)
    total_leads = sum(s.new_leads for s in stats)
    total_converted = sum(s.converted_leads for s in stats)
    
    return {
        "chart_data": chart_data,
        "summary": {
            "total_calls": total_calls,
            "total_leads": total_leads,
            "converted": total_converted,
            "conversion_rate": round((total_converted / total_leads * 100) if total_leads > 0 else 0, 1)
        }
    }
