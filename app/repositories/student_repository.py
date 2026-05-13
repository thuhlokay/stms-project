from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from app.models.student import Student
from app.schemas.student import StudentCreate


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, student_id: int) -> Optional[Student]:
        result = await self.db.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[Student]:
        result = await self.db.execute(select(Student).where(Student.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_by_student_number(self, student_number: str) -> Optional[Student]:
        result = await self.db.execute(
            select(Student).where(Student.student_number == student_number)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Student]:
        result = await self.db.execute(select(Student).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_campus(self, campus: str) -> list[Student]:
        result = await self.db.execute(
            select(Student).where(Student.campus == campus)
        )
        return list(result.scalars().all())

    async def create(self, user_id: int, student_in: StudentCreate,
                     student_card_path: str,
                     profile_picture_path: Optional[str] = None) -> Student:
        student = Student(
            user_id=user_id,
            full_name=student_in.full_name,
            student_number=student_in.student_number,
            year_level=student_in.year_level,
            course=student_in.course,
            campus=student_in.campus,
            modules=student_in.modules,
            contact_number=student_in.contact_number,
            student_card_image=student_card_path,
            profile_picture=profile_picture_path,
            popia_consent=student_in.popia_consent,
            popia_consent_at=datetime.utcnow() if student_in.popia_consent else None,
        )
        self.db.add(student)
        await self.db.flush()
        await self.db.refresh(student)
        return student

    async def delete(self, student: Student) -> None:
        await self.db.delete(student)
        await self.db.flush()
        