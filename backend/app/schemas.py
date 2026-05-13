from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    student_number: str
    
    course: str

    year_level: int

    campus: str

    phone_number: str

class LoginRequest(BaseModel):

    email: EmailStr

    password: str

class BookingRequest(BaseModel):

    tutor_id: int

    student_id: int