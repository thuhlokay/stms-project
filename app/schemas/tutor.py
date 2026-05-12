from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TutorBase(BaseModel):
    full_name: str
    student_number: str
    year_of_study: int
    modules: str
    contact_number: str
    course: str
    bio: Optional[str] = None

class TutorCreate(TutorBase):
    pass

class TutorUpdate(TutorBase):
    id: int
    user_id: int
    profile_picture: Optional[str] = None
    student_card_image: str
    academic_transcript: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class TutorResponse(TutorBase):
    id: int
    user_id: int
    profile_picture: Optional[str] = None
    student_card_image: str
    academic_transcript: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class TutorPublicResponse(BaseModel):
    id: int
    full_name: str
    student_number: str
    campus: str
    year_of_study: int
    modules: str
    course: str
    is_verified: bool
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

    model_config = {"from_attributes": True}