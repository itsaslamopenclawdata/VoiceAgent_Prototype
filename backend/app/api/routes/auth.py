"""
RepCon Voice Agent - Authentication Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.db.session import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.models.models import User

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login endpoint"""
    # Query user
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }


@router.post("/logout")
async def logout():
    """Logout endpoint (client should discard token)"""
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token():
    """Refresh access token"""
    # In production, implement proper token refresh
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not implemented"
    )


@router.post("/register")
async def register(
    email: str,
    password: str,
    full_name: str,
    institute_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Register new user"""
    # Check if email exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=email,
        password_hash=get_password_hash(password),
        full_name=full_name,
        institute_id=institute_id,
        role="admin"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role
    }
