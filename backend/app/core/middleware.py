"""
Request logging middleware for FLOW API.
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("flow.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        logger.info(
            f"{request.method} {request.url.path} "
            f"-> {response.status_code} "
            f"({duration*1000:.1f}ms)"
        )

        response.headers["X-Process-Time"] = f"{duration:.4f}"
        return response
