from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.tutor import TutorResponse, TutorPublicResponse
from app.services.tutor_service import TutorService
from app.api.v1.deps import get_current_active_user, get_current_superuser
from app.models.user import User

router = APIRouter()


@router.post("/profile", response_model=TutorResponse, status_code=201)
async def create_tutor_profile(
    full_name: str = Form(...),
    student_number: str = Form(...),
    year_level: int = Form(...),
    course: str = Form(...),
    campus: str = Form(...),
    modules: str = Form(...),
    contact_number: str = Form(...),
    student_card: UploadFile = File(...),
    transcript: UploadFile = File(...),
    profile_picture: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a tutor profile for the logged in user."""
    from app.schemas.tutor import TutorCreate
    tutor_in = TutorCreate(
        full_name=full_name,
        student_number=student_number,
        year_level=year_level,
        course=course,
        campus=campus,
        modules=modules,
        contact_number=contact_number,
    )
    service = TutorService(db)
    return await service.create_profile(
        user_id=current_user.id,
        tutor_in=tutor_in,
        student_card=student_card,
        transcript=transcript,
        profile_picture=profile_picture,
    )


@router.get("/profile/me", response_model=TutorResponse)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get the logged in tutor's own profile."""
    service = TutorService(db)
    return await service.get_my_profile(current_user.id)


@router.get("/", response_model=list[TutorPublicResponse])
async def list_tutors(
    skip: int = 0,
    limit: int = 100,
    campus: str = None,
    module: str = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """List verified tutors, optionally filter by campus or module."""
    service = TutorService(db)
    if campus:
        return await service.filter_by_campus(campus)
    if module:
        return await service.filter_by_module(module)
    return await service.list_tutors(skip=skip, limit=limit)


@router.get("/{tutor_id}", response_model=TutorPublicResponse)
async def get_tutor(
    tutor_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """Get a single tutor by ID."""
    service = TutorService(db)
    return await service.get_profile(tutor_id)


@router.post("/{tutor_id}/verify", response_model=TutorResponse)
async def verify_tutor(
    tutor_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superuser),
):
    """Verify a tutor - admin only."""
    service = TutorService(db)
    return await service.verify_tutor(tutor_id)