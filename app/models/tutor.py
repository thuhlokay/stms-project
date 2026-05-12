from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class Tutor(Base):
    __tablename__ = "tutors"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique = True, nullable=False)

    #Personal info
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    student_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    year_of_study: Mapped[int] = mapped_column(Integer, nullable=False)
    modules: Mapped[str] = mapped_column(Text, nullable=False)
    contact_number: Mapped[str] = mapped_column(String(20), nullable=False)
    course: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)

    #Files
    profile_picture: Mapped[str] = mapped_column(String(500), nullable=True)
    student_card_image: Mapped[str] = mapped_column(String(500), nullable=False)
    academic_transcript: Mapped[str] = mapped_column(String(500), nullable=False)

    #Verification
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    #Timestamps
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    user = relationship("User", backref="tutor_profile")