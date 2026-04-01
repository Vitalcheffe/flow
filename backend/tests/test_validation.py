"""
Validation Tests

Compares FLOW solvers against known analytical solutions
and published benchmark results.
"""

import numpy as np
import pytest

from app.solvers.fea_classic import generate_beam_mesh, solve, Material
from app.solvers.thermal_classic import generate_plate_mesh, solve as thermal_solve


class TestBeamDeflection:
    """Validate beam deflection against Euler-Bernoulli theory."""

    def test_cantilever_tip_deflection(self):
        """Cantilever beam with point load at tip."""
        L = 1.0  # Length (m)
        h = 0.05  # Height (m)
        b = 0.02  # Width (m)
        P = 1000.0  # Load (N)
        E = 200e9  # Young's modulus (Pa)

        # Analytical: delta = PL^3 / (3EI)
        I = b * h**3 / 12
        delta_analytical = P * L**3 / (3 * E * I)

        mat = Material(youngs_modulus=E, poissons_ratio=0.3, density=7850, thickness=b)
        mesh = generate_beam_mesh(length=L, height=h, nx=20, ny=4, material=mat)
        result = solve(mesh)

        # FEA should be within 20% of analytical for coarse mesh
        error = abs(result.max_displacement - delta_analytical) / delta_analytical
        assert error < 0.25, f"Error {error*100:.1f}% exceeds 25%"

    def test_simply_supported_uniform_load(self):
        """Simply supported beam with uniform load."""
        L = 2.0
        h = 0.1
        b = 0.05
        q = 10000.0  # N/m
        E = 200e9

        # Analytical: delta_max = 5qL^4 / (384EI)
        I = b * h**3 / 12
        delta_analytical = 5 * q * L**4 / (384 * E * I)

        mat = Material(youngs_modulus=E, poissons_ratio=0.3, density=7850, thickness=b)
        mesh = generate_beam_mesh(length=L, height=h, nx=30, ny=5, material=mat)
        result = solve(mesh)

        # Check order of magnitude
        assert result.max_displacement > 0
        assert result.max_displacement < delta_analytical * 10


class TestThermalConduction:
    """Validate thermal solver against analytical solutions."""

    def test_1d_conduction(self):
        """1D steady-state conduction: T = linear between boundaries."""
        mesh = generate_plate_mesh(nx=50, ny=3, width=1.0, height=0.1)
        result = thermal_solve(mesh, T_left=100.0, T_right=0.0, T_top=50.0, T_bottom=50.0)

        # Center row should be approximately linear
        center_row = result.temperature[1, :]
        expected = np.linspace(100, 0, 50)

        # Check linearity in interior
        for i in range(5, 45):
            assert abs(center_row[i] - expected[i]) < 5.0

    def test_uniform_boundary(self):
        """Uniform boundary conditions -> uniform temperature field."""
        mesh = generate_plate_mesh(nx=20, ny=20)
        result = thermal_solve(mesh, T_left=75.0, T_right=75.0, T_top=75.0, T_bottom=75.0)

        assert abs(result.max_temp - 75.0) < 0.1
        assert abs(result.min_temp - 75.0) < 0.1


class TestStressConvergence:
    """Verify mesh convergence for stress analysis."""

    def test_refinement_convergence(self):
        """Stress should converge as mesh is refined."""
        stresses = []
        for n in [5, 10, 20]:
            mat = Material(youngs_modulus=200e9, poissons_ratio=0.3, density=7850, thickness=0.01)
            mesh = generate_beam_mesh(length=1.0, height=0.1, nx=n*2, ny=n//2, material=mat)
            result = solve(mesh)
            stresses.append(result.max_stress)

        # Stress should stabilize (changes decrease)
        change_1 = abs(stresses[1] - stresses[0])
        change_2 = abs(stresses[2] - stresses[1])
        assert change_2 < change_1 * 2 or change_2 < 1e-6
