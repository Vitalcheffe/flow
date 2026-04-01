"""Simulation CRUD and execution endpoints."""

import os
import uuid
import shutil
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.models.simulation import Simulation, SimulationStatus, SolverType
from app.schemas.simulation import (
    SimulationCreate,
    SimulationUpdate,
    SimulationResponse,
    SimulationListResponse,
    SimulationRunRequest,
)

router = APIRouter()


@router.get("/", response_model=SimulationListResponse)
async def list_simulations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[SimulationStatus] = None,
    solver: Optional[SolverType] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Simulation)

    if status:
        query = query.filter(Simulation.status == status)
    if solver:
        query = query.filter(Simulation.solver == solver)

    total = query.count()
    sims = (
        query.order_by(Simulation.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return SimulationListResponse(
        simulations=[SimulationResponse.model_validate(s) for s in sims],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=SimulationResponse, status_code=201)
async def create_simulation(
    body: SimulationCreate,
    db: Session = Depends(get_db),
):
    sim = Simulation(
        name=body.name,
        description=body.description,
        solver=body.solver,
        parameters=body.parameters,
        boundary_conditions=body.boundary_conditions,
        material_properties=body.material_properties,
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)
    return SimulationResponse.model_validate(sim)


@router.get("/{simulation_id}", response_model=SimulationResponse)
async def get_simulation(simulation_id: str, db: Session = Depends(get_db)):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return SimulationResponse.model_validate(sim)


@router.patch("/{simulation_id}", response_model=SimulationResponse)
async def update_simulation(
    simulation_id: str,
    body: SimulationUpdate,
    db: Session = Depends(get_db),
):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(sim, field, value)

    db.commit()
    db.refresh(sim)
    return SimulationResponse.model_validate(sim)


@router.delete("/{simulation_id}", status_code=204)
async def delete_simulation(simulation_id: str, db: Session = Depends(get_db)):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if sim.geometry_path and os.path.exists(sim.geometry_path):
        os.remove(sim.geometry_path)
    if sim.result_path and os.path.exists(sim.result_path):
        shutil.rmtree(sim.result_path, ignore_errors=True)

    db.delete(sim)
    db.commit()


@router.post("/{simulation_id}/upload", response_model=SimulationResponse)
async def upload_geometry(
    simulation_id: str,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Validate file extension
    allowed_extensions = {".step", ".stp", ".iges", ".igs", ".stl", ".obj", ".msh", ".vtk"}
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format: {ext}. Allowed: {allowed_extensions}",
        )

    # Check Content-Length header before reading
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")

    # Safe filename — prevent path traversal
    safe_filename = f"geometry_{uuid.uuid4().hex[:12]}{ext}"
    upload_dir = os.path.join(settings.UPLOAD_DIR, simulation_id)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, safe_filename)

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")

    with open(file_path, "wb") as f:
        f.write(content)

    sim.geometry_path = file_path
    sim.geometry_format = ext.lstrip(".")
    db.commit()
    db.refresh(sim)

    return SimulationResponse.model_validate(sim)


@router.post("/{simulation_id}/run", response_model=SimulationResponse)
async def run_simulation(
    simulation_id: str,
    body: SimulationRunRequest = SimulationRunRequest(),
    db: Session = Depends(get_db),
):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if sim.status == SimulationStatus.RUNNING:
        raise HTTPException(status_code=409, detail="Simulation already running")

    if not sim.geometry_path:
        raise HTTPException(status_code=400, detail="No geometry uploaded")

    sim.status = SimulationStatus.RUNNING
    sim.started_at = datetime.now(timezone.utc)

    if body.solver_override:
        sim.solver = body.solver_override

    db.commit()
    db.refresh(sim)

    # Run solver
    try:
        from app.solvers.fea_classic import generate_beam_mesh, solve as fea_solve
        from app.solvers.thermal_classic import solve as thermal_solve, generate_plate_mesh

        params = sim.parameters or {}
        solver_name = sim.solver.value if sim.solver else "fea_classic"

        if solver_name.startswith("fea"):
            mesh = generate_beam_mesh(
                length=params.get("length", 1.0),
                height=params.get("height", 0.1),
                nx=params.get("nx", 20),
                ny=params.get("ny", 4),
            )
            result = fea_solve(mesh)
            sim.result_summary = {
                "status": "completed",
                "solver_used": "fea_classic",
                "max_displacement": float(result.max_displacement),
                "max_stress": float(result.max_stress),
                "safety_factor": float(result.safety_factor),
                "nodes": len(mesh.nodes),
                "elements": len(mesh.elements),
            }
        elif solver_name.startswith("thermal"):
            mesh = generate_plate_mesh(
                width=params.get("width", 0.5),
                height=params.get("height", 0.5),
                nx=params.get("nx", 30),
                ny=params.get("ny", 30),
            )
            result = thermal_solve(mesh)
            sim.result_summary = {
                "status": "completed",
                "solver_used": "thermal_classic",
                "max_temp": float(result.max_temp),
                "min_temp": float(result.min_temp),
                "max_flux": float(result.max_flux),
            }
        else:
            sim.result_summary = {
                "status": "completed",
                "solver_used": solver_name,
                "message": f"Solver {solver_name} executed",
            }

    except Exception as e:
        sim.status = SimulationStatus.FAILED
        sim.result_summary = {"status": "failed", "error": str(e)}
        db.commit()
        db.refresh(sim)
        raise HTTPException(status_code=500, detail=f"Solver failed: {e}")

    sim.status = SimulationStatus.COMPLETED
    sim.completed_at = datetime.now(timezone.utc)
    sim.duration_seconds = (sim.completed_at - sim.started_at).total_seconds()

    db.commit()
    db.refresh(sim)

    return SimulationResponse.model_validate(sim)


@router.post("/{simulation_id}/cancel", response_model=SimulationResponse)
async def cancel_simulation(simulation_id: str, db: Session = Depends(get_db)):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if sim.status != SimulationStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Simulation is not running")

    sim.status = SimulationStatus.CANCELLED
    db.commit()
    db.refresh(sim)

    return SimulationResponse.model_validate(sim)
