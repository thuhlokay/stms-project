from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, DECIMAL, Time

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False)
    student_number = Column(String(20), unique=True)
    course = Column(String(100))
    year_level = Column(Integer)
    campus = Column(String(100))
    phone_number = Column(String(20))

class TutorProfile(Base):
    __tablename__ = "tutor_profiles"

    profile_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    subjects = Column(String(200), nullable=False)
    specialization = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False)


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True)

    tutor_id = Column(Integer, ForeignKey("tutor_profiles.profile_id"))

    module_name = Column(String(100), nullable=False)

    description = Column(String)

    service_type = Column(String(50))

    duration_minutes = Column(Integer)

    cost = Column(DECIMAL(10, 2))

    is_active = Column(Boolean, default=True)

class TutorAvailability(Base):
    __tablename__ = "tutor_availability"

    availability_id = Column(Integer, primary_key=True)

    tutor_id = Column(
        Integer,
        ForeignKey("tutor_profiles.profile_id")
    )

    day_of_week = Column(String(20))

    start_time = Column(Time)

    end_time = Column(Time)

    is_available = Column(Boolean, default=True)

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)

    service_id = Column(
        Integer,
        ForeignKey("services.service_id")
    )

    student_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    tutor_id = Column(
        Integer,
        ForeignKey("tutor_profiles.profile_id")
    )

    start_datetime = Column(DateTime)

    end_datetime = Column(DateTime)

    status = Column(String(20), default="PENDING")