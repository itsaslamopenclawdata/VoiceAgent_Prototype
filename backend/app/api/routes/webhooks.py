"""
RepCon Voice Agent - Webhook Routes (Twilio)
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import httpx

from app.db.session import get_db
from app.models.models import Call, Institute, VoiceConfig

router = APIRouter()


@router.post("/twilio/voice")
async def twilio_voice_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming Twilio voice call"""
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
        # Return error TwiML
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
    
    # Return TwiML to connect to media stream
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{greeting}</Say>
    <Connect>
        <Stream url="wss://your-domain.com/media-stream" />
    </Connect>
    <Say>Thank you for calling. Goodbye!</Say>
</Response>'''


@router.post("/twilio/status")
async def twilio_status_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Twilio call status callbacks"""
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")
    
    # Find and update call
    result = await db.execute(
        select(Call).where(Call.twilio_call_sid == call_sid)
    )
    call = result.scalar_one_or_none()
    
    if call:
        call.status = call_status
        
        if call_status in ["completed", "busy", "no-answer", "failed"]:
            call.ended_at = datetime.utcnow()
            if call.started_at:
                call.duration = int((call.ended_at - call.started_at).total_seconds())
        
        await db.commit()
    
    return "OK"


@router.websocket("/media-stream")
async def media_stream(websocket):
    """WebSocket for real-time audio streaming"""
    await websocket.accept()
    
    try:
        while True:
            # Receive audio from Twilio
            data = await websocket.receive_text()
            
            # Process audio (STT -> LLM -> TTS)
            # This would integrate with the voice pipeline
            
            # Send response back
            await websocket.send_text("ack")
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
