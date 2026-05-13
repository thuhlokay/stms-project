from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.student import StudentResponse, StudentPublicResponse
from app.services.student_service import StudentService
from app.api.v1.deps import get_current_active_user, get_current_superuser
from app.models.user import User

router = APIRouter()


@router.post("/profile", response_model=StudentResponse, status_code=201)
async def create_student_profile(
    full_name: str = Form(...),
    student_number: str = Form(...),
    year_level: int = Form(...),
    course: str = Form(...),
    campus: str = Form(...),
    modules: str = Form(...),
    contact_number: str = Form(...),
    popia_consent: bool = Form(...),
    student_card: UploadFile = File(...),
    profile_picture: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a student profile for the logged in user."""
    from app.schemas.student import StudentCreate
    student_in = StudentCreate(
        full_name=full_name,
        student_number=student_number,
        year_level=year_level,
        course=course,
        campus=campus,
        modules=modules,
        contact_number=contact_number,
        popia_consent=popia_consent,
    )
    service = StudentService(db)
    return await service.create_profile(
        user_id=current_user.id,
        student_in=student_in,
        student_card=student_card,
        profile_picture=profile_picture,
    )


@router.get("/profile/me", response_model=StudentResponse)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get the logged in student's own profile."""
    service = StudentService(db)
    return await service.get_my_profile(current_user.id)


@router.get("/", response_model=list[StudentPublicResponse])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superuser),
):
    """List all students - admin only."""
    service = StudentService(db)
    return await service.list_students(skip=skip, limit=limit)


@router.get("/{student_id}", response_model=StudentPublicResponse)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """Get a student by ID."""
    service = StudentService(db)
    return await service.get_profile(student_id)