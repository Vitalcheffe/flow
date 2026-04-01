"""Simulation results endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.simulation import Simulation

router = APIRouter()


@router.get("/{simulation_id}")
async def get_results(simulation_id: str, db: Session = Depends(get_db)):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    return {
        "simulation_id": simulation_id,
        "status": sim.status.value,
        "summary": sim.result_summary,
        "solver": sim.solver.value,
        "duration_seconds": sim.duration_seconds,
    }


@router.get("/{simulation_id}/fields")
async def get_result_fields(simulation_id: str, db: Session = Depends(get_db)):
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Return available result fields based on solver type
    solver_fields = {
        "fea_classic": ["displacement", "stress_von_mises", "stress_xx", "stress_yy", "strain"],
        "fea_neural": ["displacement", "stress_von_mises", "stress_xx", "stress_yy", "strain"],
        "thermal_classic": ["temperature", "heat_flux", "gradient"],
        "thermal_neural": ["temperature", "heat_flux", "gradient"],
        "fluid_classic": ["velocity", "pressure", "vorticity"],
        "fluid_neural": ["velocity", "pressure", "vorticity"],
    }

    return {
        "simulation_id": simulation_id,
        "fields": solver_fields.get(sim.solver.value, []),
    }
