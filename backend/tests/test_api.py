"""Tests for the REST API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_version_endpoint(self):
        response = client.get("/api/v1/version")
        assert response.status_code == 200
        assert response.json()["name"] == "FLOW"


class TestSolversEndpoint:
    def test_list_solvers(self):
        response = client.get("/api/v1/solvers/")
        assert response.status_code == 200
        solvers = response.json()
        assert len(solvers) >= 4

    def test_get_specific_solver(self):
        response = client.get("/api/v1/solvers/fea_classic")
        assert response.status_code == 200
        assert response.json()["type"] == "fea_classic"


class TestSimulationsEndpoint:
    def test_list_simulations_empty(self):
        response = client.get("/api/v1/simulations/")
        assert response.status_code == 200
        data = response.json()
        assert "simulations" in data
        assert "total" in data

    def test_create_simulation(self):
        response = client.post("/api/v1/simulations/", json={
            "name": "test-beam",
            "solver": "fea_classic",
            "parameters": {"length": 1.0, "height": 0.1},
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test-beam"
        assert data["status"] == "created"

    def test_create_simulation_invalid(self):
        response = client.post("/api/v1/simulations/", json={
            "name": "",
        })
        assert response.status_code == 422

    def test_get_nonexistent_simulation(self):
        response = client.get("/api/v1/simulations/nonexistent-id")
        assert response.status_code == 404
