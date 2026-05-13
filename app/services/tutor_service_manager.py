from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.tutor_service_repository import TutorServiceRepository
from app.repositories.tutor_repository import TutorRepository
from app.schemas.tutor_service import TutorServiceCreate, TutorServiceUpdate
from app.models.tutor_service import TutorService


class TutorServiceManager:
    def __init__(self, db: AsyncSession):
        self.repo = TutorServiceRepository(db)
        self.tutor_repo = TutorRepository(db)

    async def create_service(self, user_id: int, service_in: TutorServiceCreate) -> TutorService:
        # Get tutor profile linked to this user
        tutor = await self.tutor_repo.get_by_user_id(user_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You must create a tutor profile first",
            )

        # Only verified tutors can create services (STMS-02)
        if not tutor.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your tutor profile must be verified before creating services",
            )

        return await self.repo.create(tutor_id=tutor.id, service_in=service_in)

    async def get_service(self, service_id: int) -> TutorService:
        service = await self.repo.get_by_id(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )
        return service

    async def get_my_services(self, user_id: int) -> list[TutorService]:
        tutor = await self.tutor_repo.get_by_user_id(user_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You do not have a tutor profile",
            )
        return await self.repo.get_by_tutor_id(tutor.id)

    async def get_tutor_services(self, tutor_id: int) -> list[TutorService]:
        return await self.repo.get_by_tutor_id(tutor_id)

    async def list_services(self, skip: int = 0, limit: int = 100) -> list[TutorService]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def filter_by_module(self, module: str) -> list[TutorService]:
        return await self.repo.get_by_module(module)

    async def filter_by_type(self, service_type: str) -> list[TutorService]:
        return await self.repo.get_by_service_type(service_type)

    async def update_service(self, service_id: int, user_id: int,
                              service_update: TutorServiceUpdate) -> TutorService:
        service = await self.get_service(service_id)
        tutor = await self.tutor_repo.get_by_user_id(user_id)

        # Make sure tutor owns this service
        if service.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own services",
            )

        updates = service_update.model_dump(exclude_unset=True)
        return await self.repo.update(service, updates)

    async def delete_service(self, service_id: int, user_id: int) -> None:
        service = await self.get_service(service_id)
        tutor = await self.tutor_repo.get_by_user_id(user_id)

        # Make sure tutor owns this service
        if service.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own services",
            )

        await self.repo.delete(service)