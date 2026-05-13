from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, User, TutorProfile, Booking
from app.schemas import RegisterRequest, BookingRequest, LoginRequest

import bcrypt


app = FastAPI()


origins = [
    "https://studentdoctor.co.za",
    "https://www.studentdoctor.co.za",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.get('/')
def home():
    return {
        'message': 'STMS Backend Running'
    }


@app.post('/register')
def register(data: RegisterRequest):

    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()


    if existing_user:

        return {
            'message': 'Email already exists'
        }


    hashed_password = bcrypt.hashpw(
        data.password.encode('utf-8'),
        bcrypt.gensalt()
    )


    new_user = User(
        full_name=data.full_name,

        email=data.email,

        password_hash=hashed_password.decode('utf-8'),

        role='STUDENT',

        student_number=data.student_number,

        course=data.course,

        year_level=data.year_level,

        campus=data.campus,

        phone_number=data.phone_number
    )


    db.add(new_user)

    db.commit()


    return {
        'message': 'Registration successful'
    }

@app.post('/login')
def login(data: LoginRequest):

    db: Session = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()


    if not user:

        return {
            'message': 'Invalid email or password'
        }


    password_matches = bcrypt.checkpw(
        data.password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    )


    if not password_matches:

        return {
            'message': 'Invalid email or password'
        }


    return {
        'message': 'Login successful',

        'user': {
            'user_id': user.user_id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }
    }

@app.get('/tutors')
def get_tutors():

    db: Session = SessionLocal()

    tutors = db.query(
        TutorProfile
    ).all()


    results = []

    for tutor in tutors:

        user = db.query(User).filter(
            User.user_id == tutor.user_id
        ).first()

        results.append({

            'profile_id': tutor.profile_id,

            'full_name': user.full_name,

            'specialisation':
                tutor.specialisation
        })

    return results

@app.post('/book')
def create_booking(
    data: BookingRequest
):

    db: Session = SessionLocal()


    booking = Booking(

        tutor_id=data.tutor_id,

        student_id=data.student_id,

        status='PENDING'
    )

    db.add(booking)

    db.commit()


    return {
        'message': 'Booking successful'
    }

@app.get('/seed')
def seed_data():

    db: Session = SessionLocal()

    user = User(
        full_name='John Tutor',
        email='tutor@test.com',
        password_hash='123',
        role='TUTOR'
    )

    db.add(user)

    db.commit()

    db.refresh(user)


    tutor = TutorProfile(
        user_id=user.user_id,
        specialisation='Mathematics'
    )

    db.add(tutor)

    db.commit()


    return {
        'message': 'Tutor created'
    }