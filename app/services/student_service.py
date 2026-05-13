import os
import shutil
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate
from app.models.student import Student

UPLOAD_DIR = "uploads"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]


def save_upload(file: UploadFile, folder: str) -> str:
    os.makedirs(f"{UPLOAD_DIR}/{folder}", exist_ok=True)
    file_path = f"{UPLOAD_DIR}/{folder}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    async def create_profile(
        self,
        user_id: int,
        student_in: StudentCreate,
        student_card: UploadFile,
        profile_picture: UploadFile = None,
    ) -> Student:
        # POPIA consent check (STMS-12)
        if not student_in.popia_consent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You must agree to POPIA consent to register",
            )

        # Check profile doesn't already exist
        if await self.repo.get_by_user_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student profile already exists for this user",
            )

        # Check student number is unique
        if await self.repo.get_by_student_number(student_in.student_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student number already registered",
            )

        # Validate student card
        if student_card.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student card must be a JPEG or PNG image",
            )

        # Save files
        student_card_path = save_upload(student_card, "student_cards")
        profile_picture_path = None
        if profile_picture:
            if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Profile picture must be a JPEG or PNG image",
                )
            profile_picture_path = save_upload(profile_picture, "profile_pictures")

        return await self.repo.create(
            user_id=user_id,
            student_in=student_in,
            student_card_path=student_card_path,
            profile_picture_path=profile_picture_path,
        )

    async def get_profile(self, student_id: int) -> Student:
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )
        return student

    async def get_my_profile(self, user_id: int) -> Student:
        student = await self.repo.get_by_user_id(user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You do not have a student profile yet",
            )
        return student

    async def list_students(self, skip: int = 0, limit: int = 100) -> list[Student]:
        return await self.repo.get_all(skip=skip, limit=limit)