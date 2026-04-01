"""Tests for FEA classic solver."""

import numpy as np
import pytest

from app.solvers.fea_classic import (
    generate_beam_mesh,
    solve,
    Material,
    Node,
    Element,
    BoundaryCondition,
    FEAMesh,
)


class TestBeamMesh:
    def test_generates_correct_node_count(self):
        mesh = generate_beam_mesh(length=1.0, height=0.1, nx=10, ny=2)
        assert len(mesh.nodes) == (10 + 1) * (2 + 1)  # 33 nodes

    def test_generates_correct_element_count(self):
        mesh = generate_beam_mesh(length=1.0, height=0.1, nx=10, ny=2)
        assert len(mesh.elements) == 10 * 2 * 2  # 40 elements (2 triangles per quad)

    def test_nodes_have_valid_coordinates(self):
        mesh = generate_beam_mesh(length=2.0, height=0.5, nx=5, ny=3)
        for node in mesh.nodes:
            assert 0 <= node.x <= 2.0
            assert 0 <= node.y <= 0.5

    def test_default_material_is_steel(self):
        mesh = generate_beam_mesh()
        assert mesh.material.youngs_modulus == 200e9
        assert mesh.material.poissons_ratio == 0.3

    def test_custom_material(self):
        mat = Material(
            youngs_modulus=70e9,  # Aluminum
            poissons_ratio=0.33,
            density=2700,
            thickness=0.005,
        )
        mesh = generate_beam_mesh(material=mat)
        assert mesh.material.youngs_modulus == 70e9


class TestFEASolver:
    def test_solve_returns_result(self):
        mesh = generate_beam_mesh(length=1.0, height=0.1, nx=5, ny=2)
        result = solve(mesh)

        assert result is not None
        assert len(result.displacements) == len(mesh.nodes)
        assert len(result.stresses) == len(mesh.elements)

    def test_max_displacement_is_positive(self):
        mesh = generate_beam_mesh(length=1.0, height=0.1, nx=10, ny=3)
        result = solve(mesh)
        assert result.max_displacement >= 0

    def test_max_stress_is_positive(self):
        mesh = generate_beam_mesh(length=1.0, height=0.1, nx=10, ny=3)
        result = solve(mesh)
        assert result.max_stress >= 0

    def test_safety_factor_is_positive(self):
        mesh = generate_beam_mesh(length=1.0, height=0.1, nx=10, ny=3)
        result = solve(mesh)
        assert result.safety_factor > 0

    def test_zero_load_zero_displacement(self):
        """With no loads, displacement should be zero."""
        nodes = [Node(0, 0, 0), Node(1, 1, 0), Node(2, 0.5, 0.5)]
        elements = [Element(0, [0, 1, 2])]
        material = Material(200e9, 0.3, 7850, 0.01)
        bc = [BoundaryCondition(0, ux=0, uy=0)]

        mesh = FEAMesh(nodes=nodes, elements=elements, material=material, boundary_conditions=bc)
        result = solve(mesh)

        # With fixed boundary and no load, displacement should be ~0
        for d in result.displacements:
            assert abs(d.ux) < 1e-10
            assert abs(d.uy) < 1e-10
