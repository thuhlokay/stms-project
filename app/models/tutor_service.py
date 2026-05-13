from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

from app.core.database import Base


class ServiceType(str, enum.Enum):
    PR = "PR"  # Presentation Review
    AR = "AR"  # Assignment Review
    TT = "TT"  # Topic/Module Tutoring
    PG = "PG"  # Project Guidance


class TutorService(Base):
    __tablename__ = "tutor_services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"), nullable=False)

    # Service Details
    module: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    service_type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType), nullable=False
    )
    estimated_duration: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship
    tutor = relationship("Tutor", backref="services")