"""
FLOW Backend - Engineering Simulation with AI

Main entry point for the FastAPI application.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import simulations, solvers, health, results


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    setup_logging()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.RESULTS_DIR, exist_ok=True)

    # Mount static files after directories are created
    from fastapi.staticfiles import StaticFiles
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
    app.mount("/results", StaticFiles(directory=settings.RESULTS_DIR), name="results")

    print(f"🚀 FLOW server starting on {settings.HOST}:{settings.PORT}")
    yield
    print("🛑 FLOW server shutting down")


app = FastAPI(
    title="FLOW API",
    description="Open-source engineering simulation with AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# API routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(simulations.router, prefix="/api/v1/simulations", tags=["simulations"])
app.include_router(solvers.router, prefix="/api/v1/solvers", tags=["solvers"])
app.include_router(results.router, prefix="/api/v1/results", tags=["results"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
