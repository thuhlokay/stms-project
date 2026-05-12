from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService   

router = APIRouter()

@router.post("/register", response_model = UserResponse, status_code = 201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """register a new user"""
    service = UserService(db)
    return await service.create_user(user_in)   

@router.post("/login", response_model = Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """authenticate user and return access token"""
    service = UserService(db)
    access_token = await service.authenticate(form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}