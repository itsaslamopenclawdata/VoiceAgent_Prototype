"""
RepCon Voice Agent - Webhook Routes
"""
import os
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import httpx

from app.db.session import get_db
from app.models.models import Call, Institute, VoiceConfig

router = APIRouter()

# Check if running in local-only mode
LOCAL_ONLY = os.getenv("LOCAL_ONLY", "false").lower() == "true"


@router.post("/twilio/voice")
async def twilio_voice_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming Twilio voice call"""
    if LOCAL_ONLY:
        return {'error': 'Twilio not configured. Use local mode.'}
    
    # Get call parameters
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    from_number = form_data.get("From")
    to_number = form_data.get("To")
    
    # Find institute by phone number
    result = await db.execute(
        select(Institute).where(Institute.phone_number == to_number)
    )
    institute = result.scalar_one_or_none()
    
    if not institute:
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Sorry, we could not find your institution.</Say>
</Response>'''
    
    # Get voice config
    voice_result = await db.execute(
        select(VoiceConfig).where(VoiceConfig.institute_id == institute.id)
    )
    voice_config = voice_result.scalar_one_or_none()
    
    greeting = voice_config.greeting_message if voice_config else "Hello! Welcome. How can I help you?"
    
    # Create call record
    call = Call(
        institute_id=institute.id,
        caller_phone=from_number,
        twilio_call_sid=call_sid,
        status="in_progress",
        started_at=datetime.utcnow()
    )
    db.add(call)
    await db.commit()
    await db.refresh(call)
    
    # Return TwiML
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{greeting}</Say>
    <Record maxLength="300" action="/api/v1/webhooks/twilio/recording" />
</Response>'''


@router.post("/twilio/recording")
async def twilio_recording_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Twilio recording callback"""
    if LOCAL_ONLY:
        return {'error': 'Twilio not configured'}
    
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    recording_url = form_data.get("RecordingUrl")
    
    # Update call record
    result = await db.execute(
        select(Call).where(Call.twilio_call_sid == call_sid)
    )
    call = result.scalar_one_or_none()
    
    if call:
        call.recording_url = recording_url
        await db.commit()
    
    return {'status': 'recorded'}


@router.post("/local/test-call")
async def local_test_call(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Local test endpoint - simulates a call without Twilio"""
    data = await request.json()
    
    institute_id = data.get("institute_id")
    caller_phone = data.get("caller_phone", "+919999999999")
    
    # Find institute
    result = await db.execute(
        select(Institute).where(Institute.id == institute_id)
    )
    institute = result.scalar_one_or_none()
    
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    # Create test call
    call = Call(
        institute_id=institute_id,
        caller_phone=caller_phone,
        status="completed",
        started_at=datetime.utcnow(),
        ended_at=datetime.utcnow(),
        duration=30,
        notes="Test call from local mode"
    )
    db.add(call)
    await db.commit()
    await db.refresh(call)
    
    return {
        "status": "success",
        "message": "Test call recorded",
        "call_id": call.id
    }


@router.get("/status")
async def webhook_status():
    """Check webhook status"""
    return {
        "local_only": LOCAL_ONLY,
        "twilio_configured": not LOCAL_ONLY
    }
