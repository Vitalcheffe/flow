"""
Buckling Analysis Solver

Computes critical buckling loads using eigenvalue analysis.
Solves: (K + lambda * K_sigma) * phi = 0
"""

import numpy as np
from dataclasses import dataclass
from app.solvers.fea_v2 import Node2D, Element2D, MaterialV2, assemble_global_stiffness, solve_v2


@dataclass
class BucklingResult:
    critical_loads: np.ndarray  # Eigenvalues (load multipliers)
    mode_shapes: np.ndarray  # Buckling mode shapes
    n_modes: int

    @property
    def min_load_factor(self) -> float:
        return float(self.critical_loads[0]) if len(self.critical_loads) > 0 else float('inf')


def geometric_stiffness_beam(
    nodes: list[Node2D],
    elements: list[Element2D],
    mat: MaterialV2,
    reference_load: np.ndarray,
) -> np.ndarray:
    """Compute geometric stiffness matrix from reference stress state."""
    n_dof = 2 * len(nodes)
    Kg = np.zeros((n_dof, n_dof))

    # Solve linear problem to get stress state
    result = solve_v2(nodes, elements, mat)
    disp = result["displacements"]

    # Simplified geometric stiffness for beam elements
    for elem in elements:
        n0, n1 = elem.node_ids[0], elem.node_ids[1]
        x0, y0 = nodes[n0].x, nodes[n0].y
        x1, y1 = nodes[n1].x, nodes[n1].y

        L = np.sqrt((x1-x0)**2 + (y1-y0)**2)
        if L < 1e-10:
            continue

        # Axial force from displacement
        du = disp[n1, 0] - disp[n0, 0]
        N = mat.E * mat.t * du / L  # Axial force

        # Geometric stiffness contribution
        kg = N / (30 * L) * np.array([
            [36, 3*L, -36, 3*L],
            [3*L, 4*L**2, -3*L, -L**2],
            [-36, -3*L, 36, -3*L],
            [3*L, -L**2, -3*L, 4*L**2],
        ])

        dofs = [2*n0, 2*n0+1, 2*n1, 2*n1+1]
        for i, gi in enumerate(dofs):
            for j, gj in enumerate(dofs):
                Kg[gi, gj] += kg[i, j]

    return Kg


def solve_buckling(
    nodes: list[Node2D],
    elements: list[Element2D],
    mat: MaterialV2,
    n_modes: int = 3,
) -> BucklingResult:
    """
    Solve linear buckling eigenvalue problem.

    Returns critical load factors and buckling mode shapes.
    """
    # Elastic stiffness
    K = assemble_global_stiffness(nodes, elements, mat)

    # Geometric stiffness (simplified)
    n_dof = K.shape[0]
    ref_load = np.zeros(n_dof)
    for node in nodes:
        ref_load[2*node.id] = node.fx
        ref_load[2*node.id + 1] = node.fy

    Kg = geometric_stiffness_beam(nodes, elements, mat, ref_load)

    # Find fixed DOFs
    fixed_dofs = []
    for node in nodes:
        if node.ux_fixed:
            fixed_dofs.append(2 * node.id)
        if node.uy_fixed:
            fixed_dofs.append(2 * node.id + 1)

    free_dofs = [i for i in range(n_dof) if i not in fixed_dofs]

    if not free_dofs:
        return BucklingResult(critical_loads=np.array([]), mode_shapes=np.array([]), n_modes=0)

    K_ff = K[np.ix_(free_dofs, free_dofs)]
    Kg_ff = Kg[np.ix_(free_dofs, free_dofs)]

    # Solve: (K + lambda * Kg) * phi = 0
    # Equivalent to: K * phi = -lambda * Kg * phi
    try:
        eigenvalues, eigenvectors = np.linalg.eigh(-Kg_ff, K_ff + 1e-12 * np.eye(len(free_dofs)))
    except np.linalg.LinAlgError:
        return BucklingResult(critical_loads=np.array([]), mode_shapes=np.array([]), n_modes=0)

    # Filter positive eigenvalues (physical buckling loads)
    positive = eigenvalues > 1e-6
    eigenvalues = eigenvalues[positive]
    eigenvectors = eigenvectors[:, positive]

    # Sort ascending
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx][:n_modes]
    eigenvectors = eigenvectors[:, idx][:, :n_modes]

    # Expand to full DOF
    full_shapes = np.zeros((n_dof, len(eigenvalues)))
    for i, dof in enumerate(free_dofs):
        if i < eigenvectors.shape[0]:
            full_shapes[dof, :] = eigenvectors[i, :]

    return BucklingResult(
        critical_loads=eigenvalues,
        mode_shapes=full_shapes,
        n_modes=len(eigenvalues),
    )
