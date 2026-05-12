import time
import logging
from urllib import request
from starlette.responses import response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("uvicorn.access")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start_time) * 1000

        logger.info(f"{request.method} {request.url.path}" f" ->{response.status_code} [{duration:.2f}ms]")
        return response