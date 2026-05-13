from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user