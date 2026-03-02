"""
RepCon Voice Agent - Settings Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import VoiceConfig, Institute

router = APIRouter()


@router.get("/")
async def get_settings(
    institute_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get institute settings"""
    # Get institute
    institute_result = await db.execute(
        select(Institute).where(Institute.id == institute_id)
    )
    institute = institute_result.scalar_one_or_none()
    
    if not institute:
        return {"error": "Institute not found"}
    
    # Get voice config
    voice_result = await db.execute(
        select(VoiceConfig).where(VoiceConfig.institute_id == institute_id)
    )
    voice_config = voice_result.scalar_one_or_none()
    
    return {
        "institute": {
            "name": institute.name,
            "phone_number": institute.phone_number,
            "email": institute.email,
            "address": institute.address,
            "logo_url": institute.logo_url,
            "website": institute.website,
            "google_sheet_url": institute.google_sheet_url,
            "timezone": institute.timezone
        },
        "voice": {
            "greeting_message": voice_config.greeting_message if voice_config else None,
            "goodbye_message": voice_config.goodbye_message if voice_config else None,
            "language": voice_config.language if voice_config else "en",
            "voice_id": voice_config.voice_id if voice_config else None,
            "max_call_duration": voice_config.max_call_duration if voice_config else 300,
            "enable_recording": voice_config.enable_recording if voice_config else False,
            "enable_transcription": voice_config.enable_transcription if voice_config else True
        }
    }


@router.put("/")
async def update_settings(
    institute_id: int = Query(...),
    # Institute settings
    name: Optional[str] = None,
    phone_number: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    google_sheet_url: Optional[str] = None,
    # Voice settings
    greeting_message: Optional[str] = None,
    goodbye_message: Optional[str] = None,
    language: Optional[str] = None,
    voice_id: Optional[str] = None,
    max_call_duration: Optional[int] = None,
    enable_recording: Optional[bool] = None,
    enable_transcription: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update institute settings"""
    # Update institute
    institute_result = await db.execute(
        select(Institute).where(Institute.id == institute_id)
    )
    institute = institute_result.scalar_one_or_none()
    
    if not institute:
        return {"error": "Institute not found"}
    
    if name:
        institute.name = name
    if phone_number:
        institute.phone_number = phone_number
    if email:
        institute.email = email
    if address:
        institute.address = address
    if google_sheet_url:
        institute.google_sheet_url = google_sheet_url
    
    # Update voice config
    voice_result = await db.execute(
        select(VoiceConfig).where(VoiceConfig.institute_id == institute_id)
    )
    voice_config = voice_result.scalar_one_or_none()
    
    if voice_config:
        if greeting_message:
            voice_config.greeting_message = greeting_message
        if goodbye_message:
            voice_config.goodbye_message = goodbye_message
        if language:
            voice_config.language = language
        if voice_id:
            voice_config.voice_id = voice_id
        if max_call_duration:
            voice_config.max_call_duration = max_call_duration
        if enable_recording is not None:
            voice_config.enable_recording = enable_recording
        if enable_transcription is not None:
            voice_config.enable_transcription = enable_transcription
    
    await db.commit()
    
    return {"message": "Settings updated successfully"}
