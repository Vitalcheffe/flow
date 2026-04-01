"""Tests for CFD solver."""

import numpy as np
import pytest

from app.solvers.cfd import solve_cavity_flow, CFDResult


class TestCavityFlow:
    def test_returns_result(self):
        result = solve_cavity_flow(nx=11, ny=11, max_iter=10)
        assert isinstance(result, CFDResult)

    def test_velocity_shape(self):
        result = solve_cavity_flow(nx=21, ny=21, max_iter=5)
        assert result.u.shape == (21, 21)
        assert result.v.shape == (21, 21)

    def test_pressure_shape(self):
        result = solve_cavity_flow(nx=21, ny=21, max_iter=5)
        assert result.p.shape == (21, 21)

    def test_lid_velocity(self):
        result = solve_cavity_flow(nx=11, ny=11, u_lid=1.0, max_iter=5)
        assert np.allclose(result.u[-1, :], 1.0)

    def test_wall_no_slip(self):
        result = solve_cavity_flow(nx=11, ny=11, max_iter=5)
        assert np.allclose(result.u[0, :], 0.0)  # bottom
        assert np.allclose(result.u[:, 0], 0.0)  # left
        assert np.allclose(result.u[:, -1], 0.0)  # right
        assert np.allclose(result.v[0, :], 0.0)
        assert np.allclose(result.v[-1, :], 0.0)

    def test_iterations_positive(self):
        result = solve_cavity_flow(nx=11, ny=11, max_iter=100)
        assert result.iterations > 0
