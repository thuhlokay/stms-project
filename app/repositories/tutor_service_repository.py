from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.models.tutor_service import TutorService
from app.schemas.tutor_service import TutorServiceCreate


class TutorServiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, service_id: int) -> Optional[TutorService]:
        result = await self.db.execute(
            select(TutorService).where(TutorService.id == service_id)
        )
        return result.scalar_one_or_none()

    async def get_by_tutor_id(self, tutor_id: int) -> list[TutorService]:
        result = await self.db.execute(
            select(TutorService).where(TutorService.tutor_id == tutor_id)
        )
        return list(result.scalars().all())

    async def get_by_module(self, module: str) -> list[TutorService]:
        result = await self.db.execute(
            select(TutorService).where(TutorService.module == module)
        )
        return list(result.scalars().all())

    async def get_by_service_type(self, service_type: str) -> list[TutorService]:
        result = await self.db.execute(
            select(TutorService).where(TutorService.service_type == service_type)
        )
        return list(result.scalars().all())

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[TutorService]:
        result = await self.db.execute(
            select(TutorService).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, tutor_id: int, service_in: TutorServiceCreate) -> TutorService:
        service = TutorService(
            tutor_id=tutor_id,
            module=service_in.module,
            description=service_in.description,
            service_type=service_in.service_type,
            estimated_duration=service_in.estimated_duration,
            cost=service_in.cost,
        )
        self.db.add(service)
        await self.db.flush()
        await self.db.refresh(service)
        return service

    async def update(self, service: TutorService, updates: dict) -> TutorService:
        for key, value in updates.items():
            setattr(service, key, value)
        await self.db.flush()
        await self.db.refresh(service)
        return service

    async def delete(self, service: TutorService) -> None:
        await self.db.delete(service)
        await self.db.flush()