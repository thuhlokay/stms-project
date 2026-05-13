from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, tutors, students, tutor_services

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tutors.router, prefix="/tutors", tags=["Tutors"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(tutor_services.router, prefix="/services", tags=["Tutor Services"])