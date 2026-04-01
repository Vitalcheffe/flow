"""Tests for thermal solver."""

import numpy as np
import pytest

from app.solvers.thermal_classic import (
    generate_plate_mesh,
    solve,
    ThermalMaterial,
)


class TestThermalMesh:
    def test_generates_correct_dimensions(self):
        mesh = generate_plate_mesh(width=1.0, height=0.5, nx=50, ny=25)
        assert mesh["nx"] == 50
        assert mesh["ny"] == 25
        assert mesh["dx"] == pytest.approx(1.0 / 49)
        assert mesh["dy"] == pytest.approx(0.5 / 24)

    def test_default_material_is_steel(self):
        mesh = generate_plate_mesh()
        assert mesh["material"].thermal_conductivity == 50.0


class TestThermalSolver:
    def test_solve_returns_result(self):
        mesh = generate_plate_mesh(nx=20, ny=20)
        result = solve(mesh)

        assert result.temperature.shape == (20, 20)
        assert result.heat_flux_x.shape == (20, 20)
        assert result.heat_flux_y.shape == (20, 20)

    def test_boundary_conditions_applied(self):
        mesh = generate_plate_mesh(nx=20, ny=20)
        result = solve(mesh, T_left=100.0, T_right=20.0)

        assert result.temperature[10, 0] == pytest.approx(100.0, abs=0.1)
        assert result.temperature[10, -1] == pytest.approx(20.0, abs=0.1)

    def test_temperature_between_boundaries(self):
        mesh = generate_plate_mesh(nx=30, ny=30)
        result = solve(mesh, T_left=100.0, T_right=0.0)

        interior = result.temperature[1:-1, 1:-1]
        assert np.all(interior >= -1.0)
        assert np.all(interior <= 101.0)

    def test_uniform_boundary_uniform_field(self):
        mesh = generate_plate_mesh(nx=20, ny=20)
        result = solve(mesh, T_left=50.0, T_right=50.0, T_top=50.0, T_bottom=50.0)

        assert np.allclose(result.temperature, 50.0, atol=0.1)
