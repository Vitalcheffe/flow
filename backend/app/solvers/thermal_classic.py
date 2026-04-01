"""
Thermal Classic Solver

Implements basic heat transfer analysis using finite difference method.
Supports steady-state 2D conduction problems.
"""

import numpy as np
from dataclasses import dataclass, field


@dataclass
class ThermalMaterial:
    thermal_conductivity: float  # W/(m*K)
    density: float  # kg/m3
    specific_heat: float  # J/(kg*K)


@dataclass
class ThermalBoundaryCondition:
    type: str  # "fixed_temp", "flux", "convection"
    value: float
    nodes: list[int] = field(default_factory=list)


@dataclass
class ThermalMesh:
    nx: int
    ny: int
    dx: float
    dy: float
    material: ThermalMaterial
    boundary_conditions: list[ThermalBoundaryCondition] = field(default_factory=list)


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
) -> ThermalMesh:
    """Generate a rectangular plate thermal mesh."""
    if material is None:
        material = ThermalMaterial(
            thermal_conductivity=50.0,  # Steel
            density=7850,
            specific_heat=460,
        )

    return ThermalMesh(
        nx=nx,
        ny=ny,
        dx=width / (nx - 1),
        dy=height / (ny - 1),
        material=material,
        boundary_conditions=[
            ThermalBoundaryCondition(type="fixed_temp", value=100.0, nodes=[0]),
            ThermalBoundaryCondition(type="fixed_temp", value=20.0, nodes=[1]),
        ],
    )


def solve(mesh: ThermalMesh, T_left: float = 100.0, T_right: float = 20.0,
          T_top: float = 50.0, T_bottom: float = 50.0) -> ThermalResult:
    """
    Solve steady-state 2D heat conduction using finite differences.
    """
    nx, ny = mesh.nx, mesh.ny
    T = np.ones((ny, nx)) * 25.0  # Initial temperature

    # Boundary conditions
    T[:, 0] = T_left    # Left
    T[:, -1] = T_right  # Right
    T[0, :] = T_top     # Top
    T[-1, :] = T_bottom # Bottom

    # Iterative solver (Gauss-Seidel)
    k = mesh.material.thermal_conductivity
    max_iter = 10000
    tolerance = 1e-6

    for iteration in range(max_iter):
        T_old = T.copy()

        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                T[i, j] = 0.25 * (
                    T[i-1, j] + T[i+1, j] +
                    T[i, j-1] + T[i, j+1]
                )

        # Check convergence
        error = np.max(np.abs(T - T_old))
        if error < tolerance:
            break

    # Compute heat flux
    qx = -k * np.gradient(T, mesh.dx, axis=1)
    qy = -k * np.gradient(T, mesh.dy, axis=0)
    q_mag = np.sqrt(qx**2 + qy**2)

    return ThermalResult(
        temperature=T,
        heat_flux_x=qx,
        heat_flux_y=qy,
        max_temp=float(np.max(T)),
        min_temp=float(np.min(T)),
        max_flux=float(np.max(q_mag)),
    )
