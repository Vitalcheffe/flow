"""Pydantic schemas for simulation API."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.models.simulation import SimulationStatus, SolverType


class SimulationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    solver: SolverType = SolverType.FEA_CLASSIC
    parameters: Dict[str, Any] = {}
    boundary_conditions: Dict[str, Any] = {}
    material_properties: Dict[str, Any] = {}


class SimulationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    solver: Optional[SolverType] = None
    parameters: Optional[Dict[str, Any]] = None
    boundary_conditions: Optional[Dict[str, Any]] = None
    material_properties: Optional[Dict[str, Any]] = None


class SimulationResponse(BaseModel):
    id: str
    name: str
    description: str
    solver: SolverType
    status: SimulationStatus
    geometry_format: Optional[str]
    parameters: Dict[str, Any]
    boundary_conditions: Dict[str, Any]
    material_properties: Dict[str, Any]
    result_summary: Dict[str, Any]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    mesh_elements: Optional[int]
    mesh_nodes: Optional[int]

    class Config:
        from_attributes = True


class SimulationListResponse(BaseModel):
    simulations: List[SimulationResponse]
    total: int
    page: int
    page_size: int


class SolverInfo(BaseModel):
    name: str
    type: str
    description: str
    speedup: str
    use_case: str
    available: bool


class SimulationRunRequest(BaseModel):
    solver_override: Optional[SolverType] = None
    parameters_override: Optional[Dict[str, Any]] = None


class ResultFieldResponse(BaseModel):
    field_name: str
    field_type: str
    min_value: Optional[float]
    max_value: Optional[float]
    mean_value: Optional[float]

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    version: str
    gpu_available: bool
    active_simulations: int
