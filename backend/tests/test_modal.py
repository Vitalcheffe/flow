"""Tests for modal analysis solver."""

import numpy as np
import pytest

from app.solvers.modal import solve_modal, lumped_mass_matrix
from app.solvers.fea_v2 import Node2D, Element2D, MaterialV2


class TestModalAnalysis:
    def _make_mesh(self, nx=3, ny=2):
        nodes = []
        idx = 0
        for j in range(ny + 1):
            for i in range(nx + 1):
                nodes.append(Node2D(idx, i * 0.5, j * 0.2))
                idx += 1

        elements = []
        eid = 0
        for j in range(ny):
            for i in range(nx):
                n0 = j * (nx + 1) + i
                elements.append(Element2D(eid, [n0, n0 + 1, n0 + nx + 2, n0 + nx + 1]))
                eid += 1

        return nodes, elements

    def test_returns_frequencies(self):
        nodes, elements = self._make_mesh()
        mat = MaterialV2(E=200e9, nu=0.3)
        result = solve_modal(nodes, elements, mat, n_modes=3)
        assert len(result.frequencies_hz) > 0

    def test_frequencies_positive(self):
        nodes, elements = self._make_mesh()
        mat = MaterialV2(E=200e9, nu=0.3)
        result = solve_modal(nodes, elements, mat, n_modes=3)
        assert np.all(result.frequencies_hz > 0)

    def test_frequencies_sorted(self):
        nodes, elements = self._make_mesh()
        mat = MaterialV2(E=200e9, nu=0.3)
        result = solve_modal(nodes, elements, mat, n_modes=4)
        assert np.all(np.diff(result.frequencies_hz) >= -1e-6)
