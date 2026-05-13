from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.api.v1.deps import get_current_active_user, get_current_active_superuser
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model = UserResponse)
async def get_current_user(current_user: user = Depends(get_current_active_user)):
    """get current authenticated user"""
    return current_user

@router.get("/users", response_model = list[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: user = Depends(get_current_active_superuser)):
    """list all users (superuser only)"""
    service = UserService(db)
    return await service.list_users(skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model = UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_active_user),):
    """get user by id (authenticated users only)"""
    service = UserService(db)
    return await service.get_user(user_id)