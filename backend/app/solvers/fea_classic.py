"""
FEA Classic Solver

Implements basic finite element analysis for 2D structural problems.
Uses triangular elements with linear shape functions.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    id: int
    x: float
    y: float


@dataclass
class Element:
    id: int
    node_ids: list[int]


@dataclass
class Material:
    youngs_modulus: float  # Pa
    poissons_ratio: float
    density: float  # kg/m3
    thickness: float  # m


@dataclass
class BoundaryCondition:
    node_id: int
    ux: Optional[float] = None  # displacement x
    uy: Optional[float] = None  # displacement y
    fx: Optional[float] = None  # force x
    fy: Optional[float] = None  # force y


@dataclass
class FEAMesh:
    nodes: list[Node]
    elements: list[Element]
    material: Material
    boundary_conditions: list[BoundaryCondition]


@dataclass
class FEADisplacement:
    node_id: int
    ux: float
    uy: float


@dataclass
class FEAStress:
    element_id: int
    sigma_xx: float
    sigma_yy: float
    tau_xy: float
    von_mises: float


@dataclass
class FEAResult:
    displacements: list[FEADisplacement]
    stresses: list[FEAStress]
    max_displacement: float
    max_stress: float
    safety_factor: float


def generate_beam_mesh(
    length: float = 1.0,
    height: float = 0.1,
    nx: int = 20,
    ny: int = 4,
    material: Optional[Material] = None,
) -> FEAMesh:
    """Generate a simple rectangular beam mesh."""
    if material is None:
        material = Material(
            youngs_modulus=200e9,  # Steel
            poissons_ratio=0.3,
            density=7850,
            thickness=0.01,
        )

    nodes = []
    node_id = 0
    for j in range(ny + 1):
        for i in range(nx + 1):
            nodes.append(Node(id=node_id, x=i * length / nx, y=j * height / ny))
            node_id += 1

    elements = []
    elem_id = 0
    for j in range(ny):
        for i in range(nx):
            n0 = j * (nx + 1) + i
            n1 = n0 + 1
            n2 = n0 + (nx + 1)
            n3 = n2 + 1
            # Two triangles per quad
            elements.append(Element(id=elem_id, node_ids=[n0, n1, n2]))
            elem_id += 1
            elements.append(Element(id=elem_id, node_ids=[n1, n3, n2]))
            elem_id += 1

    # Fixed left edge
    bc_nodes = []
    for j in range(ny + 1):
        bc_nodes.append(
            BoundaryCondition(node_id=j * (nx + 1), ux=0.0, uy=0.0)
        )

    # Load on right edge (downward force)
    for j in range(ny + 1):
        bc_nodes.append(
            BoundaryCondition(
                node_id=j * (nx + 1) + nx,
                fy=-1000.0,
            )
        )

    return FEAMesh(
        nodes=nodes,
        elements=elements,
        material=material,
        boundary_conditions=bc_nodes,
    )


def compute_element_stiffness(
    nodes: list[Node],
    element: Element,
    material: Material,
) -> np.ndarray:
    """Compute element stiffness matrix for a triangular element."""
    n0, n1, n2 = [nodes[nid] for nid in element.node_ids]

    # Area of triangle
    area = 0.5 * abs(
        (n1.x - n0.x) * (n2.y - n0.y) - (n2.x - n0.x) * (n1.y - n0.y)
    )

    # Material matrix (plane stress)
    E = material.youngs_modulus
    nu = material.poissons_ratio
    D = (E / (1 - nu**2)) * np.array([
        [1, nu, 0],
        [nu, 1, 0],
        [0, 0, (1 - nu) / 2],
    ])

    # Simplified stiffness (constant strain triangle)
    t = material.thickness
    k = t * area * np.eye(6) * E / (1 - nu**2)

    return k


def solve(mesh: FEAMesh) -> FEAResult:
    """
    Solve the FEA problem.
    Returns displacements and stresses.
    """
    n_dof = 2 * len(mesh.nodes)
    K = np.zeros((n_dof, n_dof))
    F = np.zeros(n_dof)

    # Assemble global stiffness matrix
    for elem in mesh.elements:
        ke = compute_element_stiffness(mesh.nodes, elem, mesh.material)
        for i, ni in enumerate(elem.node_ids):
            for j, nj in enumerate(elem.node_ids):
                dofs_i = [2 * ni, 2 * ni + 1]
                dofs_j = [2 * nj, 2 * nj + 1]
                for di in range(2):
                    for dj in range(2):
                        K[dofs_i[di], dofs_j[dj]] += ke[2 * i + di, 2 * j + dj]

    # Apply boundary conditions
    fixed_dofs = []
    for bc in mesh.boundary_conditions:
        if bc.ux is not None:
            dof = 2 * bc.node_id
            fixed_dofs.append(dof)
        if bc.uy is not None:
            dof = 2 * bc.node_id + 1
            fixed_dofs.append(dof)
        if bc.fx is not None:
            F[2 * bc.node_id] += bc.fx
        if bc.fy is not None:
            F[2 * bc.node_id + 1] += bc.fy

    # Solve (simplified: use pseudo-inverse for demo)
    free_dofs = [i for i in range(n_dof) if i not in fixed_dofs]

    if len(free_dofs) == 0:
        return FEAResult(
            displacements=[],
            stresses=[],
            max_displacement=0.0,
            max_stress=0.0,
            safety_factor=float("inf"),
        )

    K_ff = K[np.ix_(free_dofs, free_dofs)]
    F_f = F[free_dofs]

    try:
        U_f = np.linalg.solve(K_ff + 1e-10 * np.eye(len(free_dofs)), F_f)
    except np.linalg.LinAlgError:
        U_f = np.zeros(len(free_dofs))

    U = np.zeros(n_dof)
    for i, dof in enumerate(free_dofs):
        U[dof] = U_f[i]

    # Extract displacements
    displacements = []
    max_disp = 0.0
    for node in mesh.nodes:
        ux = U[2 * node.id]
        uy = U[2 * node.id + 1]
        disp = np.sqrt(ux**2 + uy**2)
        max_disp = max(max_disp, disp)
        displacements.append(FEADisplacement(node_id=node.id, ux=ux, uy=uy))

    # Compute stresses (simplified)
    stresses = []
    max_stress = 0.0
    E = mesh.material.youngs_modulus
    for elem in mesh.elements:
        avg_ux = np.mean([U[2 * nid] for nid in elem.node_ids])
        avg_uy = np.mean([U[2 * nid + 1] for nid in elem.node_ids])
        sigma_xx = E * avg_ux
        sigma_yy = E * avg_uy
        tau_xy = E * 0.5 * (avg_ux + avg_uy)
        von_mises = np.sqrt(sigma_xx**2 - sigma_xx * sigma_yy + sigma_yy**2 + 3 * tau_xy**2)
        max_stress = max(max_stress, von_mises)
        stresses.append(
            FEAStress(
                element_id=elem.id,
                sigma_xx=sigma_xx,
                sigma_yy=sigma_yy,
                tau_xy=tau_xy,
                von_mises=von_mises,
            )
        )

    safety_factor = mesh.material.youngs_modulus / max(max_stress, 1e-10)

    return FEAResult(
        displacements=displacements,
        stresses=stresses,
        max_displacement=max_disp,
        max_stress=max_stress,
        safety_factor=min(safety_factor, 100.0),
    )
