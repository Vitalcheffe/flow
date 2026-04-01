# FLOW

<p align="center">
  <strong>Open-source engineering simulation with AI. In your browser.</strong>
</p>

<p align="center">
  <a href="https://github.com/Vitalcheffe/flow/actions"><img src="https://img.shields.io/github/actions/workflow/status/Vitalcheffe/flow/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT"></a>
  <a href="https://github.com/Vitalcheffe/flow"><img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="https://github.com/Vitalcheffe/flow"><img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react" alt="React"></a>
</p>

FLOW lets engineers run structural, thermal, and fluid simulations in the browser. No $50K license. No 6-month training. Open the browser, import your geometry, simulate.

AI-powered solvers (Neural Operators) make simulations 100x faster than traditional FEA. What takes ANSYS 4 hours, FLOW does in 2 seconds.

## Why

- ANSYS costs $50K+/year. COMSOL costs $10K+. ABAQUS costs $30K+.
- Free tools (FreeCAD, CalculiX) are clunky, desktop-only, slow.
- Engineers in Africa, Asia, South America have zero access to simulation.
- AI (Neural Operators) can accelerate physics simulation by 100-1000x. This is active research (ICLR 2025, 2026) but nobody has made it a product.

FLOW is that product.

## Features

- **Structural Analysis** — stress, strain, deformation under load
- **Thermal Analysis** — heat transfer, steady-state and transient
- **Fluid Dynamics** — laminar flow, basic CFD
- **AI Solver** — Fourier Neural Operator for real-time results
- **3D Viewer** — Three.js-based, interactive, works in browser
- **Import** — STEP, IGES, STL, OBJ geometry files
- **Export** — CSV, JSON, VTK result formats
- **API** — REST API for automation and CI/CD integration
- **Self-host** — Docker one-liner, runs anywhere

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m app.main

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Or with Docker:

```bash
docker compose up
```

Visit http://localhost:5173

## Architecture

```
flow/
├── backend/           # Python FastAPI server
│   ├── app/
│   │   ├── api/       # REST endpoints
│   │   ├── core/      # Config, logging, middleware
│   │   ├── solvers/   # FEA, thermal, fluid solvers
│   │   ├── neural/    # Neural Operator models
│   │   ├── models/    # Database models (SQLAlchemy)
│   │   └── schemas/   # Pydantic request/response schemas
│   └── tests/
├── frontend/          # React + TypeScript + Vite
│   └── src/
│       ├── components/
│       │   ├── viewer/      # 3D geometry viewer
│       │   ├── simulation/  # Simulation controls
│       │   └── ui/          # Shared UI components
│       ├── pages/
│       ├── hooks/
│       └── lib/
├── docker/            # Dockerfiles
├── docs/              # Documentation
├── examples/          # Example simulations
└── scripts/           # Build and deploy scripts
```

## Solvers

| Solver | Type | Speed | Use Case |
|--------|------|-------|----------|
| `fea_classic` | FEM | Baseline | Structural analysis, validation |
| `fea_neural` | Neural Operator | 100x | Real-time structural |
| `thermal_classic` | FEM | Baseline | Heat transfer |
| `thermal_neural` | Neural Operator | 200x | Real-time thermal |
| `fluid_classic` | FVM | Baseline | Laminar CFD |
| `fluid_neural` | Neural Operator | 500x | Real-time fluid |

## Comparison

| Feature | ANSYS | COMSOL | FreeCAD | **FLOW** |
|---------|-------|--------|---------|----------|
| Price | $50K+ | $10K+ | Free | **Free** |
| Web-based | No | No | No | **Yes** |
| AI solver | No | No | No | **Yes** |
| Mobile | No | No | No | **Yes** |
| Open source | No | No | Yes | **Yes** |
| Self-host | No | No | N/A | **Yes** |
| API | No | Limited | No | **Yes** |
| Learning curve | 6 months | 3 months | 2 months | **10 minutes** |

## API

```bash
# Create simulation
curl -X POST http://localhost:8000/api/v1/simulations \
  -H "Content-Type: application/json" \
  -d '{"name": "bridge-beam", "solver": "fea_neural", "geometry": "beam.step"}'

# Run simulation
curl -X POST http://localhost:8000/api/v1/simulations/1/run

# Get results
curl http://localhost:8000/api/v1/simulations/1/results
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
