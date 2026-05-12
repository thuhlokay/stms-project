from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate

class TutorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tutor_id: int) -> Optional[Tutor]:
        result = await self.db.execute(select(Tutor).where(Tutor.id == tutor_id))
        return result.scalars_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[Tutor]:
        result =  await self.db.execute(select(Tutor).where(Tutor.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_by_student_number(self, student_number: str) -> Optional[Tutor]:
        result = await self.db.execute(select(Tutor).where(Tutor.student_number == student_number))
        return result.scalar_one_or_none()  
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Tutor]:
        result = await self.db.execute(select(Tutor).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def get_verified_tutors(self, skip: int = 0, limit: int = 100) -> list[Tutor]:
        result = await self.db.execute(select(Tutor).where(Tutor.is_verified == True).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_campus(self, campus:str) -> list[Tutor]:
        result = await self.db.execute(select(Tutor).where(Tutor.campus == campus, Tutor.is_verified == True))
        return list(result.scalars().all())
    
    async def get_by_module(self, module: str) -> list[Tutor]:
        result = await self.db.execute(select(Tutor).where(Tutor.modules.contains(module), Tutor.is_verified == True))
        return list(result.scalars().all())

    async def create(self, user_id: int, tutor_in: TutorCreate, student_card_path: str, 
                    transcript_path: str, profile_picture_path: Optional[str] = None) -> Tutor:
        tutor = Tutor(user_id=user_id,
                      full_name=tutor_in.full_name,
                      student_number=tutor_in.student_number,
                      year_of_study=tutor_in.year_of_study,
                      course=tutor_in.course,
                      modules=tutor_in.modules,
                      campus=tutor_in.campus,
                      contact_number=tutor_in.contact_number,
                      student_card_image=student_card_path,
                      academic_transcript=transcript_path,
                      profile_picture=profile_picture_path,
                      bio=tutor_in.bio)
        self.db.add(tutor)
        await self.db.flush()
        await self.db.refresh(tutor)
        return tutor
    
    async def verify(self, tutor: Tutor) -> Tutor:
        tutor.is_verified = True
        tutor.verified_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(tutor)
        return tutor
    
    async def delete(self, tutor: Tutor) -> None:
        await self.db.delete(tutor)
        await self.db.flush()