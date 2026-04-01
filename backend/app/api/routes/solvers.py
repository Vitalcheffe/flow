"""Available solvers endpoint."""

from fastapi import APIRouter

from app.schemas.simulation import SolverInfo

router = APIRouter()

SOLVERS = [
    SolverInfo(
        name="FEA Classic",
        type="fea_classic",
        description="Traditional finite element analysis for structural problems",
        speedup="1x (baseline)",
        use_case="Structural analysis: stress, strain, deformation",
        available=True,
    ),
    SolverInfo(
        name="FEA Neural",
        type="fea_neural",
        description="AI-accelerated structural analysis using Fourier Neural Operators",
        speedup="100x",
        use_case="Real-time structural prediction",
        available=False,
    ),
    SolverInfo(
        name="Thermal Classic",
        type="thermal_classic",
        description="Classical heat transfer solver (steady-state and transient)",
        speedup="1x (baseline)",
        use_case="Thermal analysis: conduction, convection, radiation",
        available=True,
    ),
    SolverInfo(
        name="Thermal Neural",
        type="thermal_neural",
        description="AI-accelerated thermal prediction",
        speedup="200x",
        use_case="Real-time thermal mapping",
        available=False,
    ),
    SolverInfo(
        name="Fluid Classic",
        type="fluid_classic",
        description="Classical CFD solver for laminar flows",
        speedup="1x (baseline)",
        use_case="Fluid dynamics: velocity, pressure fields",
        available=False,
    ),
    SolverInfo(
        name="Fluid Neural",
        type="fluid_neural",
        description="AI-accelerated fluid dynamics using Neural Operators",
        speedup="500x",
        use_case="Real-time flow prediction",
        available=False,
    ),
]


@router.get("/", response_model=list[SolverInfo])
async def list_solvers():
    return SOLVERS


@router.get("/{solver_type}", response_model=SolverInfo)
async def get_solver(solver_type: str):
    for solver in SOLVERS:
        if solver.type == solver_type:
            return solver
    return {"error": "Solver not found"}
