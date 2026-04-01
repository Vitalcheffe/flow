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
    u: np.ndarray
    v: np.ndarray
    p: np.ndarray
    iterations: int
    residual: float


def solve_cavity_flow(
    nx: int = 41,
    ny: int = 41,
    Re: float = 100.0,
    u_lid: float = 1.0,
    rho: float = 1.0,
    max_iter: int = 5000,
    tolerance: float = 1e-4,
) -> CFDResult:
    """Solve lid-driven cavity flow (vectorized)."""
    dx = 1.0 / (nx - 1)
    dy = 1.0 / (ny - 1)
    nu = u_lid / Re

    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    u[-1, :] = u_lid

    dt = 0.001

    for iteration in range(max_iter):
        u_old = u.copy()
        v_old = v.copy()

        un = u.copy()
        vn = v.copy()

        # Vectorized momentum equations
        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            - dt * (
                un[1:-1, 1:-1] * (un[1:-1, 1:-1] - un[1:-1, :-2]) / dx
                + vn[1:-1, 1:-1] * (un[1:-1, 1:-1] - un[:-2, 1:-1]) / dy
            )
            + nu * dt * (
                (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2]) / dx**2
                + (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1]) / dy**2
            )
        )

        v[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            - dt * (
                un[1:-1, 1:-1] * (vn[1:-1, 1:-1] - vn[1:-1, :-2]) / dx
                + vn[1:-1, 1:-1] * (vn[1:-1, 1:-1] - vn[:-2, 1:-1]) / dy
            )
            + nu * dt * (
                (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, :-2]) / dx**2
                + (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[:-2, 1:-1]) / dy**2
            )
        )

        # Boundary conditions
        u[0, :] = 0; u[:, 0] = 0; u[:, -1] = 0; u[-1, :] = u_lid
        v[0, :] = 0; v[:, 0] = 0; v[:, -1] = 0; v[-1, :] = 0

        # Vectorized pressure correction (Jacobi iteration)
        for _ in range(50):
            pn = p.copy()
            p[1:-1, 1:-1] = (
                (pn[1:-1, 2:] + pn[1:-1, :-2]) * dy**2
                + (pn[2:, 1:-1] + pn[:-2, 1:-1]) * dx**2
                - rho * dx**2 * dy**2 / dt * (
                    (u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx)
                    + (v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)
                )
            ) / (2 * (dx**2 + dy**2))

            p[0, :] = p[1, :]
            p[-1, :] = p[-2, :]
            p[:, 0] = p[:, 1]
            p[:, -1] = p[:, -2]

        residual = np.max(np.abs(u - u_old)) + np.max(np.abs(v - v_old))
        if residual < tolerance:
            return CFDResult(u=u, v=v, p=p, iterations=iteration + 1, residual=residual)

    return CFDResult(u=u, v=v, p=p, iterations=max_iter, residual=residual)
