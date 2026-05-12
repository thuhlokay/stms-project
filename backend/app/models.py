from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False)
    student_number = Column(String(20), unique=True)

    class TutorProfile(Base):
        __tablename__ = "tutor_profiles"

        profile_id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.user_id"))
        subjects = Column(String(200), nullable=False)
        specialization = Column(String(100), nullable=False)
        is_verified = Column(Boolean, default=False)