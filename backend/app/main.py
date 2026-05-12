from fastapi import FastAPI

from sqlalchemy import text

from app.database import engine
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

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

@app.get("/")
def home():

    return {"message": "STMS backend is running"}

from sqlalchemy import text
from app.database import engine


@app.get("/tables")
def get_tables():

    with engine.connect() as connection:

        result = connection.execute(
            text(
                "SELECT tablename FROM pg_tables WHERE schemaname='public';"
            )
        )

        tables = [row[0] for row in result]

    return {"tables": tables}