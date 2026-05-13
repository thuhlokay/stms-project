from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import verify_password, create_access_token


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
        if await self.repo.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        if await self.repo.get_by_username(user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        return await self.repo.create(user_in)

    async def authenticate(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )
        return create_access_token(subject=user.id)

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repo.get_all(skip=skip, limit=limit)