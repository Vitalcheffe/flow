# Solvers package

from app.solvers.fea_classic import (
    generate_beam_mesh,
    solve as fea_solve,
    Material,
    FEAMesh,
    FEAResult,
)

from app.solvers.thermal_classic import (
    generate_plate_mesh,
    solve as thermal_solve,
    ThermalMaterial,
    ThermalMesh,
    ThermalResult,
)

__all__ = [
    "generate_beam_mesh",
    "fea_solve",
    "Material",
    "FEAMesh",
    "FEAResult",
    "generate_plate_mesh",
    "thermal_solve",
    "ThermalMaterial",
    "ThermalMesh",
    "ThermalResult",
]
