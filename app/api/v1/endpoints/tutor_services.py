from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.tutor_service import TutorServiceCreate, TutorServiceUpdate, TutorServiceResponse
from app.services.tutor_service_manager import TutorServiceManager
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=TutorServiceResponse, status_code=201)
async def create_service(
    service_in: TutorServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new tutoring service - verified tutors only."""
    manager = TutorServiceManager(db)
    return await manager.create_service(user_id=current_user.id, service_in=service_in)


@router.get("/my", response_model=list[TutorServiceResponse])
async def get_my_services(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all services created by the logged in tutor."""
    manager = TutorServiceManager(db)
    return await manager.get_my_services(user_id=current_user.id)


@router.get("/", response_model=list[TutorServiceResponse])
async def list_services(
    skip: int = 0,
    limit: int = 100,
    module: str = None,
    service_type: str = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """List all services, optionally filter by module or service type."""
    manager = TutorServiceManager(db)
    if module:
        return await manager.filter_by_module(module)
    if service_type:
        return await manager.filter_by_type(service_type)
    return await manager.list_services(skip=skip, limit=limit)


@router.get("/tutor/{tutor_id}", response_model=list[TutorServiceResponse])
async def get_tutor_services(
    tutor_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """Get all services offered by a specific tutor."""
    manager = TutorServiceManager(db)
    return await manager.get_tutor_services(tutor_id=tutor_id)


@router.get("/{service_id}", response_model=TutorServiceResponse)
async def get_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """Get a single service by ID."""
    manager = TutorServiceManager(db)
    return await manager.get_service(service_id=service_id)


@router.put("/{service_id}", response_model=TutorServiceResponse)
async def update_service(
    service_id: int,
    service_update: TutorServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a service - only the tutor who created it can update."""
    manager = TutorServiceManager(db)
    return await manager.update_service(
        service_id=service_id,
        user_id=current_user.id,
        service_update=service_update,
    )


@router.delete("/{service_id}", status_code=204)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a service - only the tutor who created it can delete."""
    manager = TutorServiceManager(db)
    await manager.delete_service(service_id=service_id, user_id=current_user.id)