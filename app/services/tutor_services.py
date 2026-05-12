import os
import shutil
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tutor_repository import TutorRepository
from app.schemas.tutor import TutorCreate
from app.models.tutor import Tutor

UPLOAD_DIR = "uploads"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "image/jpeg", "image/png"]

def save_upload(file: UploadFile, folder: str) -> str:
    os.makedirs(f"{UPLOAD_DIR}/{folder}", exist_ok = True)
    file_path = f"{UPLOAD_DIR}/{folder}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return file_path

class TuturService:
    def __init__(self, db: AsyncSession):
        self.repo = TutorRepository(db)

    async def create_profile(
        self,
        user_id: int,
        student_card: UploadFile,
        transcript: UploadFile,
        profile_picture: UploadFile = None,
    ) -> Tutor:

        if await self.repo.get_by_user_id(user_id):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Tutor profile already exists for this user",
            )

        if await self.repo.get_by_student_number(tutor_in.student_number):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Student number already registered",
            )   

        if student_card.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code =  status.HTTP_400_BAD_REQUEST,
                detail = "Student card must be in a JPEG or PNG format",
            )
        if transcript.content_type not in ALLOWED_DOCUMENT_TYPES:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Transcript must be in a PDF, JPEG or PNG format",
            )

        student_card_path = save_upload(student_card, "student_cards")
        transcript_path = save_upload(transcript, "transcripts")
        profile_picture_path = None
        if profile_picture:
            if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Profile picture must be in a JPEG or PNG format",
                )
                profile_picture_path = save_upload(profile_picture, "profile_pictures")

            return await self.repo.create(
                user_id = user_id,
                tutor_in = tutor_in,
                student_card_path = student_card_path,
                transcript_path = transcript_path,
                profile_picture_path = profile_picture_path,
            )

    async def get_profile(self, tutor_id: int) -> Tutor:
        tutor = await self.repo.get_by_id(tutor_id)
        if not tutor:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Tutor not found",
            )
        return tutor

    async def get_my_profile(self, user_id: int)-> Tutor:
            tutor = await self.repo .get_by_user_id(user_id)
            if not tutor:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "You do not have a tutor profile yet",
                )
            return tutor

    async def list_tutors(self, skip: int = 0, limit = 100) -> list[Tutor]:
            return await self.repo.get_verified(skip = skip, limit = limit)
        
    async def filter_by_campus(self, campus: str) -> list[Tutor]:
            return await self.repo.get_by_campus(campus)

        async def filter_by_module(self, module: str) -> list[Tutor]:
            return await self.repo.get_by_module(module)

        async def verify_tutor(self, tutor_id: int) -> Tutor:
            tutor = await self.repo.get_by_id(tutor_id)
            if not tutor:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Tutor not found",
                )
            if tutor.is_verified:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Tutor is already verified",
                )
            return await self.repo.verify(tutor)
