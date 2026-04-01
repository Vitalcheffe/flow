# CHANGELOG

## v0.1.0 (2026-04-01)

### Features
- FastAPI backend with REST API
- FEA classic solver (triangular elements, plane stress)
- FEA v2 solver (quadrilateral elements, plane stress/strain)
- Thermal classic solver (2D heat conduction, finite differences)
- CFD solver (2D lid-driven cavity flow, SIMPLE algorithm)
- Modal analysis solver (natural frequencies and mode shapes)
- Linear buckling analysis solver
- Fourier Neural Operator (FNO) architecture for AI-accelerated solving
- Neural operator training pipeline
- Material library (8 common engineering materials)
- Geometry parsers (STL ASCII/binary, OBJ)
- Mesh generators (rectangular, circular, L-shaped)
- Result visualization utilities (colormaps, VTK export)
- Request logging and rate limiting middleware
- Background task queue system

### Frontend
- React 18 + TypeScript + Vite + Tailwind CSS 4
- Dashboard with simulation management
- New simulation page with solver selection
- Simulation detail page with run/delete/results
- Solvers page with comparison table
- Landing page with hero and feature showcase
- 3D geometry viewer (Three.js)
- Result charts (Recharts)
- Responsive layout with mobile navigation
- Health status badge
- Error boundary

### Infrastructure
- Docker deployment (backend + frontend + nginx)
- CI/CD with GitHub Actions
- Development setup script
- Issue templates (bug report, feature request)
- Contributing guide
- Deployment guide
- API reference documentation
- Project roadmap

### Tests
- FEA solver tests (beam mesh, stiffness matrix)
- Thermal solver tests (boundary conditions, convergence)
- API endpoint tests (CRUD, health check)
- Mesh generation tests (rectangular, circular, L-shape)
- Visualization tests (colormaps, VTK export)
- Geometry parser tests (STL, OBJ, generators)
- FEA v2 tests (material matrix, shape functions)
- Validation tests (analytical comparison)

### Examples
- Beam deflection analysis
- Thermal plate simulation
- Cantilever beam with convergence study
- Thermal transient cooling analysis
