"""
Thermal Classic Solver

2D heat transfer analysis using vectorized finite differences.
"""

import numpy as np
from dataclasses import dataclass, field


@dataclass
class ThermalMaterial:
    thermal_conductivity: float
    density: float
    specific_heat: float


@dataclass
class ThermalResult:
    temperature: np.ndarray
    heat_flux_x: np.ndarray
    heat_flux_y: np.ndarray
    max_temp: float
    min_temp: float
    max_flux: float


def generate_plate_mesh(
    width: float = 0.5,
    height: float = 0.5,
    nx: int = 50,
    ny: int = 50,
    material: ThermalMaterial | None = None,
) -> dict:
    """Generate a rectangular plate thermal mesh."""
    if material is None:
        material = ThermalMaterial(
            thermal_conductivity=50.0,
            density=7850,
            specific_heat=460,
        )
    return {"nx": nx, "ny": ny, "dx": width / (nx - 1), "dy": height / (ny - 1), "material": material}


def solve(
    mesh: dict,
    T_left: float = 100.0,
    T_right: float = 20.0,
    T_top: float = 50.0,
    T_bottom: float = 50.0,
) -> ThermalResult:
    """Solve steady-state 2D heat conduction (vectorized)."""
    nx, ny = mesh["nx"], mesh["ny"]
    k = mesh["material"].thermal_conductivity
    T = np.full((ny, nx), 25.0)

    # Boundary conditions
    T[:, 0] = T_left
    T[:, -1] = T_right
    T[0, :] = T_top
    T[-1, :] = T_bottom

    max_iter = 10000
    tolerance = 1e-6

    for _ in range(max_iter):
        T_old = T.copy()

        # Vectorized Gauss-Seidel (Jacobi for simplicity)
        T[1:-1, 1:-1] = 0.25 * (
            T_old[:-2, 1:-1] + T_old[2:, 1:-1] +
            T_old[1:-1, :-2] + T_old[1:-1, 2:]
        )

        if np.max(np.abs(T - T_old)) < tolerance:
            break

    dx = mesh["dx"]
    dy = mesh["dy"]
    qx = -k * np.gradient(T, dx, axis=1)
    qy = -k * np.gradient(T, dy, axis=0)
    q_mag = np.sqrt(qx**2 + qy**2)

    return ThermalResult(
        temperature=T,
        heat_flux_x=qx,
        heat_flux_y=qy,
        max_temp=float(np.max(T)),
        min_temp=float(np.min(T)),
        max_flux=float(np.max(q_mag)),
    )
