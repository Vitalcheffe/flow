"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "gpu_available": False,
        "active_simulations": 0,
    }


@router.get("/version")
async def version():
    return {"version": "0.1.0", "name": "FLOW"}
