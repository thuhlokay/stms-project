from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class ServiceType(str, Enum):
    PR = "PR"  # Presentation Review
    AR = "AR"  # Assignment Review
    TT = "TT"  # Topic/Module Tutoring
    PG = "PG"  # Project Guidance


class TutorServiceBase(BaseModel):
    module: str
    description: str
    service_type: ServiceType
    estimated_duration: str
    cost: Optional[float] = None


class TutorServiceCreate(TutorServiceBase):
    pass


class TutorServiceUpdate(BaseModel):
    module: Optional[str] = None
    description: Optional[str] = None
    service_type: Optional[ServiceType] = None
    estimated_duration: Optional[str] = None
    cost: Optional[float] = None


class TutorServiceResponse(TutorServiceBase):
    id: int
    tutor_id: int
    created_at: datetime

    model_config = {"from_attributes": True}