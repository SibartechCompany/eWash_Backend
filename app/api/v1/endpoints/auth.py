from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, get_current_active_user
from app.crud.user import user as crud_user
from app.schemas.token import Token
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import User

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Login with email and password, get an access token for future requests
    """
    user = await crud_user.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not await crud_user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    # Convertir el usuario a diccionario para la respuesta
    user_data = {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.value if hasattr(user.role, 'value') else str(user.role),
        "status": "active" if user.is_active else "inactive",
        "organization_id": str(user.organization_id) if user.organization_id else None,
        "phone": user.phone,
        "avatar_url": None,  # No está en el modelo actual
        "last_login": None,  # No está en el modelo actual
        "is_verified": user.email_verified,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data
    )

@router.get("/me", response_model=User)
async def get_current_user(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user information
    """
    return current_user

@router.get("/test-token", response_model=User)
async def test_token(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Test access token
    """
    return current_user 