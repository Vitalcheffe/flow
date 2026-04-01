"""Tests for advanced FEA solver."""

import numpy as np
import pytest

from app.solvers.fea_v2 import (
    Node2D,
    Element2D,
    MaterialV2,
    ElementType,
    AnalysisType,
    material_matrix,
    shape_functions_quad,
    element_stiffness_quad,
    solve_v2,
)


class TestMaterialMatrix:
    def test_plane_stress_symmetry(self):
        mat = MaterialV2(E=200e9, nu=0.3)
        D = material_matrix(mat, AnalysisType.PLANE_STRESS)
        assert np.allclose(D, D.T)

    def test_plane_stress_positive_definite(self):
        mat = MaterialV2(E=200e9, nu=0.3)
        D = material_matrix(mat, AnalysisType.PLANE_STRESS)
        eigenvalues = np.linalg.eigvalsh(D)
        assert np.all(eigenvalues > 0)

    def test_plane_strain_stiffer(self):
        mat = MaterialV2(E=200e9, nu=0.3)
        D_stress = material_matrix(mat, AnalysisType.PLANE_STRESS)
        D_strain = material_matrix(mat, AnalysisType.PLANE_STRAIN)
        assert D_strain[0, 0] > D_stress[0, 0]


class TestShapeFunctions:
    def test_partition_of_unity(self):
        for xi in [-0.5, 0, 0.5]:
            for eta in [-0.5, 0, 0.5]:
                N, _ = shape_functions_quad(xi, eta)
                assert abs(sum(N) - 1.0) < 1e-10

    def test_corner_values(self):
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for i, (xi, eta) in enumerate(corners):
            N, _ = shape_functions_quad(xi, eta)
            assert abs(N[i] - 1.0) < 1e-10
            for j in range(4):
                if j != i:
                    assert abs(N[j]) < 1e-10


class TestElementStiffness:
    def test_symmetric(self):
        coords = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
        mat = MaterialV2(E=200e9, nu=0.3)
        Ke = element_stiffness_quad(coords, mat)
        assert np.allclose(Ke, Ke.T, atol=1e-6)

    def test_positive_semidefinite(self):
        coords = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
        mat = MaterialV2(E=200e9, nu=0.3)
        Ke = element_stiffness_quad(coords, mat)
        eigenvalues = np.linalg.eigvalsh(Ke)
        assert np.all(eigenvalues > -1e-6)


class TestSolveV2:
    def test_fixed_beam(self):
        nodes = [
            Node2D(0, 0, 0, ux_fixed=True, uy_fixed=True),
            Node2D(1, 1, 0, ux_fixed=True, uy_fixed=True),
            Node2D(2, 1, 0.1),
            Node2D(3, 0, 0.1, fy=-1000),
        ]
        elements = [Element2D(0, [0, 1, 2, 3])]
        mat = MaterialV2(E=200e9, nu=0.3)

        result = solve_v2(nodes, elements, mat)
        assert result["max_disp"] >= 0
        assert result["max_stress"] >= 0
