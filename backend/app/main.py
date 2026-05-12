from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, User
from app.schemas import RegisterRequest

import bcrypt


app = FastAPI()


origins = [
    "https://studentdoctor.co.za"
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