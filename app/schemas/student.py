from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StudentBase(BaseModel):
    full_name: str
    student_number: str
    year_level: int
    course: str
    campus: str
    modules: str
    contact_number: str


class StudentCreate(StudentBase):
    popia_consent: bool


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    year_level: Optional[int] = None
    course: Optional[str] = None
    campus: Optional[str] = None
    modules: Optional[str] = None
    contact_number: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    user_id: int
    profile_picture: Optional[str] = None
    student_card_image: str
    popia_consent: bool
    popia_consent_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class StudentPublicResponse(BaseModel):
    id: int
    full_name: str
    student_number: str
    campus: str
    course: str
    year_level: int
    modules: str

    model_config = {"from_attributes": True}