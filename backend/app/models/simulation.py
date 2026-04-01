"""SQLAlchemy models for FLOW."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, Enum as SAEnum, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
import enum


class SimulationStatus(str, enum.Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SolverType(str, enum.Enum):
    FEA_CLASSIC = "fea_classic"
    FEA_NEURAL = "fea_neural"
    THERMAL_CLASSIC = "thermal_classic"
    THERMAL_NEURAL = "thermal_neural"
    FLUID_CLASSIC = "fluid_classic"
    FLUID_NEURAL = "fluid_neural"


def generate_uuid():
    return str(uuid.uuid4())


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    solver = Column(SAEnum(SolverType), default=SolverType.FEA_CLASSIC)
    status = Column(SAEnum(SimulationStatus), default=SimulationStatus.CREATED)

    # Geometry
    geometry_path = Column(String(512), nullable=True)
    geometry_format = Column(String(20), nullable=True)
    geometry_metadata = Column(JSON, default=dict)

    # Simulation parameters
    parameters = Column(JSON, default=dict)
    boundary_conditions = Column(JSON, default=dict)
    material_properties = Column(JSON, default=dict)

    # Results
    result_path = Column(String(512), nullable=True)
    result_summary = Column(JSON, default=dict)

    # Timing
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Performance
    mesh_elements = Column(Integer, nullable=True)
    mesh_nodes = Column(Integer, nullable=True)
    iterations = Column(Integer, nullable=True)


class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    simulation_id = Column(String, nullable=False, index=True)

    # Result data
    field_name = Column(String(100), nullable=False)
    field_type = Column(String(50), nullable=False)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)
    mean_value = Column(Float, nullable=True)

    # Full data (stored as JSON for small meshes, file path for large)
    data_path = Column(String(512), nullable=True)
    data_inline = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
