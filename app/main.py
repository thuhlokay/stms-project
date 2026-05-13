import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_tables

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await create_tables()
    yield
    print("Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} → {response.status_code} [{duration:.1f}ms]")
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": settings.VERSION}