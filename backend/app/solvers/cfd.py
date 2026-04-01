"""
CFD Solver — 2D Laminar Flow (SIMPLE Algorithm)

Computes velocity and pressure fields for incompressible
laminar flow using the SIMPLE (Semi-Implicit Method for
Pressure-Linked Equations) algorithm.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class CFDResult:
    u: np.ndarray  # x-velocity
    v: np.ndarray  # y-velocity
    p: np.ndarray  # pressure
    iterations: int
    residual: float


def solve_cavity_flow(
    nx: int = 41,
    ny: int = 41,
    Re: float = 100.0,
    u_lid: float = 1.0,
    max_iter: int = 5000,
    tolerance: float = 1e-4,
) -> CFDResult:
    """
    Solve lid-driven cavity flow.

    Classic CFD benchmark: square cavity with moving top wall.
    """
    dx = 1.0 / (nx - 1)
    dy = 1.0 / (ny - 1)
    nu = u_lid / Re  # kinematic viscosity

    # Initialize fields
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))

    # Lid velocity
    u[-1, :] = u_lid

    dt = 0.001

    for iteration in range(max_iter):
        u_old = u.copy()
        v_old = v.copy()

        # Momentum equations (explicit)
        un = u.copy()
        vn = v.copy()

        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                # u-momentum
                u[i, j] = (un[i, j] -
                    dt * (un[i, j] * (un[i, j] - un[i, j-1]) / dx +
                          vn[i, j] * (un[i, j] - un[i-1, j]) / dy) +
                    nu * dt * (
                        (un[i, j+1] - 2*un[i, j] + un[i, j-1]) / dx**2 +
                        (un[i+1, j] - 2*un[i, j] + un[i-1, j]) / dy**2))

                # v-momentum
                v[i, j] = (vn[i, j] -
                    dt * (un[i, j] * (vn[i, j] - vn[i, j-1]) / dx +
                          vn[i, j] * (vn[i, j] - vn[i-1, j]) / dy) +
                    nu * dt * (
                        (vn[i, j+1] - 2*vn[i, j] + vn[i, j-1]) / dx**2 +
                        (vn[i+1, j] - 2*vn[i, j] + vn[i-1, j]) / dy**2))

        # Boundary conditions
        u[0, :] = 0; u[:, 0] = 0; u[:, -1] = 0; u[-1, :] = u_lid
        v[0, :] = 0; v[:, 0] = 0; v[:, -1] = 0; v[-1, :] = 0

        # Pressure correction (Poisson equation)
        for _ in range(50):
            pn = p.copy()
            for i in range(1, ny - 1):
                for j in range(1, nx - 1):
                    p[i, j] = (
                        (pn[i, j+1] + pn[i, j-1]) * dy**2 +
                        (pn[i+1, j] + pn[i-1, j]) * dx**2 -
                        rho * dx**2 * dy**2 / (2 * (dx**2 + dy**2)) *
                        (1/dt * ((u[i, j+1] - u[i, j-1]) / (2*dx) +
                                 (v[i+1, j] - v[i-1, j]) / (2*dy)))
                    ) / (2 * (dx**2 + dy**2)) * (dx**2 * dy**2)
            p[0, :] = p[1, :]; p[-1, :] = p[-2, :]; p[:, 0] = p[:, 1]; p[:, -1] = p[:, -2]

        # Check convergence
        residual = np.max(np.abs(u - u_old)) + np.max(np.abs(v - v_old))
        if residual < tolerance:
            return CFDResult(u=u, v=v, p=p, iterations=iteration+1, residual=residual)

    return CFDResult(u=u, v=v, p=p, iterations=max_iter, residual=residual)


rho = 1.0  # density
