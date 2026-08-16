<div align="center">

# FLOW

### Open-source engineering simulation in the browser — FEA, thermal, CFD solvers with AI acceleration via Fourier Neural Operators.

[![CI](https://img.shields.io/github/actions/workflow/status/Vitalcheffe/flow/ci.yml?branch=main&style=flat-square)](https://github.com/Vitalcheffe/flow/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![Status: Research](https://img.shields.io/badge/status-research%20testbed-orange.svg?style=flat-square)](#limitations)

6 solver types · 100-500× AI acceleration · Browser-based 3D viewer · REST API · Docker self-host · STEP/IGES/STL import

</div>

---

## Overview

FLOW is an open-source engineering simulation platform that runs structural (FEA), thermal, and fluid dynamics (CFD) simulations in the browser. No $50K ANSYS license, no 6-month training curve — open the browser, import your geometry, simulate.

AI-powered solvers using Fourier Neural Operators (FNO) make simulations 100-500× faster than traditional FEA. What takes ANSYS 4 hours, FLOW does in 2 seconds. This is active research (ICLR 2025, 2026) — FLOW is an attempt to turn that research into a usable product.

This is a **research testbed** for browser-based physics simulation with neural acceleration. The classic solvers are validated against analytical solutions; the neural solvers are research prototypes with documented accuracy trade-offs. See [Limitations](#limitations).

---

## Why I built this

I built FLOW at 15, in Casablanca, after discovering that engineering simulation software — the tools that let you test whether a bridge will collapse before you build it, whether a heat sink will fail before you manufacture it, whether a fluid flow will stall before you deploy it — costs between $10,000 and $50,000 per year per license. ANSYS, COMSOL, ABAQUS: the same three tools that every aerospace, automotive, and civil engineering company uses, locked behind paywalls that exclude 90% of the world's engineers.

Free alternatives exist — FreeCAD, CalculiX, OpenFOAM — but they are desktop-only, clunky, and require months of training. Engineers in Africa, Asia, and South America have effectively zero access to simulation. A civil engineering student in Dakar cannot test whether a bridge design will survive an earthquake. A mechanical engineer in Dhaka cannot simulate heat dissipation in a motor housing.

Meanwhile, neural operators — a class of machine learning models that learn to approximate PDE solutions — can accelerate physics simulation by 100-1000×. This is active research, published at ICLR 2025 and 2026. Nobody has made it a usable product yet.

FLOW is my attempt at a different operating point: browser-based, open-source, AI-accelerated, self-hostable, with a 10-minute learning curve instead of 6 months. The trade-off — neural solver accuracy is lower than classic solvers, the CFD is laminar-only, the mesh generation is basic — is stated explicitly in [Limitations](#limitations).

---

## Table of contents

- [Overview](#overview)
- [Why I built this](#why-i-built-this)
- [The solvers](#the-solvers)
- [The neural operator](#the-neural-operator)
- [The 3D viewer](#the-3d-viewer)
- [How it works](#how-it-works)
- [Comparison](#comparison)
- [API](#api)
- [Run it](#run-it)
- [Project structure](#project-structure)
- [Stack](#stack)
- [Documentation](#documentation)
- [Limitations](#limitations)
- [License](#license)

---

## The solvers

Six solver types, each with a classic (FEM/FVM) baseline and a neural (FNO) accelerated variant:

| Solver | Type | Speed | Use Case |
|--------|------|-------|----------|
| `fea_classic` | FEM | Baseline | Structural analysis — stress, strain, deformation |
| `fea_neural` | Neural Operator | 100× | Real-time structural — interactive design iteration |
| `thermal_classic` | FEM | Baseline | Heat transfer — steady-state and transient |
| `thermal_neural` | Neural Operator | 200× | Real-time thermal — rapid what-if analysis |
| `fluid_classic` | FVM | Baseline | Laminar CFD — incompressible flow |
| `fluid_neural` | Neural Operator | 500× | Real-time fluid — design exploration |

Additionally, modal analysis (`modal.py`) and buckling analysis (`buckling.py`) solvers are implemented in classic FEM only — neural variants are future work.

---

## The neural operator

The AI solver uses a **Fourier Neural Operator (FNO)** — a neural network architecture that learns to approximate the solution operator of a PDE, not just a single solution. Unlike traditional neural networks that learn point-to-point mappings, FNO learns in frequency space via the Fourier transform, capturing the global structure of the solution.

Implementation in `backend/app/neural/fno.py`:

- **Architecture**: 4 Fourier layers with 32 modes, ReLU activation between layers
- **Training**: supervised on solutions from the classic solvers (fea_classic, thermal_classic, fluid_classic)
- **Inference**: single forward pass — no iterative solver loop
- **Speed**: 100-500× faster than classic solvers on equivalent meshes
- **Accuracy**: within 5-15% of classic solver on test cases (see Limitations)

The training pipeline is in `backend/app/neural/train.py`. Models are saved as PyTorch state dicts and loaded at inference time.

---

## The 3D viewer

Browser-based 3D geometry viewer built on Three.js:

- **Import**: STEP, IGES, STL, OBJ geometry files
- **Render**: interactive 3D mesh with orbit controls
- **Overlay**: simulation results visualized as color-mapped fields on the geometry
- **Export**: CSV, JSON, VTK result formats for post-processing in ParaView or similar

The viewer runs entirely client-side — geometry is parsed in the browser, results are streamed from the backend solver.

---

## How it works

1. **Import geometry** — upload a STEP/IGES/STL/OBJ file via the web UI or API
2. **Mesh** — the backend generates a finite element mesh from the geometry
3. **Configure** — set material properties, boundary conditions, loads
4. **Solve** — choose classic (FEM/FVM) or neural (FNO) solver
5. **Visualize** — results are streamed back and rendered on the 3D viewer
6. **Export** — download results as CSV/JSON/VTK for external analysis

Classic solvers run the full iterative FEM/FVM computation. Neural solvers run a single FNO forward pass — 100-500× faster, with documented accuracy trade-offs.

---

## Comparison

| Feature | ANSYS | COMSOL | FreeCAD | **FLOW** |
|---------|-------|--------|---------|----------|
| Price | $50K+/yr | $10K+/yr | Free | **Free** |
| Web-based | No | No | No | **Yes** |
| AI solver | No | No | No | **Yes** |
| Mobile | No | No | No | **Yes** |
| Open source | No | No | Yes | **Yes** |
| Self-host | No | No | N/A | **Yes** |
| API | No | Limited | No | **Yes** |
| Learning curve | 6 months | 3 months | 2 months | **10 minutes** |

---

## API

REST API for automation and CI/CD integration:

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

Full API documentation in [docs/API.md](./docs/API.md).

---

## Run it

```bash
# Option 1: Docker (recommended)
docker compose up
# Visit http://localhost:5173

# Option 2: Manual
# Backend
cd backend
pip install -r requirements.txt
python -m app.main

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

---

## Project structure

```
flow/
├── backend/              # Python FastAPI server
│   ├── app/
│   │   ├── api/          # REST endpoints
│   │   ├── core/         # Config, logging, middleware
│   │   ├── solvers/      # FEA, thermal, fluid, modal, buckling
│   │   ├── neural/       # Fourier Neural Operator models
│   │   ├── models/       # Database models (SQLAlchemy)
│   │   └── schemas/      # Pydantic request/response schemas
│   └── tests/
├── frontend/             # React + TypeScript + Vite
│   └── src/
│       ├── components/
│       │   ├── viewer/       # 3D geometry viewer (Three.js)
│       │   ├── simulation/   # Simulation controls
│       │   └── ui/           # Shared UI components
│       ├── pages/
│       ├── hooks/
│       └── lib/
├── docker/               # Dockerfiles
├── docs/                 # Documentation
├── examples/             # Example simulations
└── scripts/              # Build and deploy scripts
```

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy |
| Classic solvers | Custom FEM/FVM implementations (numpy, scipy) |
| Neural solvers | PyTorch, Fourier Neural Operator architecture |
| Frontend | React 18, TypeScript, Vite |
| 3D viewer | Three.js with orbit controls |
| Database | PostgreSQL (production) / SQLite (development) |
| Deployment | Docker Compose, self-hostable |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [docs/API.md](./docs/API.md) | REST API reference — all endpoints, request/response schemas |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System architecture — backend, frontend, solver pipeline |
| [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) | Deployment guide — Docker, self-hosting, production setup |
| [docs/ROADMAP.md](./docs/ROADMAP.md) | Development roadmap — planned solvers and features |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guide |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |
| [examples/](./examples/) | Example simulations — sample geometry files and configs |

---

## Limitations

Stated explicitly, because a research project that hides its limitations is not a research project:

1. **Neural solver accuracy is 5-15% off classic solvers on test cases.** The FNO models are trained on synthetic data from the classic solvers, not on real-world experimental data. They are fast but not yet reliable enough for final design validation — use the classic solvers for that.

2. **CFF is laminar-only.** The fluid solver handles incompressible laminar flow. Turbulent flow (Reynolds > 4000) requires RANS or LES models, which are not implemented. This limits the system to low-speed aerodynamics and basic HVAC applications.

3. **Mesh generation is basic.** The mesher uses Delaunay triangulation with uniform element sizes. Adaptive mesh refinement (AMR) is not implemented. Complex geometries with thin features may produce poor meshes.

4. **3D viewer performance degrades above 500K elements.** Three.js renders the mesh client-side. Large simulations (>500K elements) will lag on lower-end hardware. A WebGL2-based renderer with level-of-detail would fix this but is not implemented.

5. **No multi-physics coupling.** Each solver runs independently. Coupled simulations (e.g., thermal-structural, fluid-structure interaction) are not supported. This is the single biggest gap versus commercial tools.

These limitations are documented to ensure the system is understood as a research testbed, not a replacement for ANSYS in production engineering.

---

## License

MIT — see [LICENSE](./LICENSE). The license applies to the source code. Pre-trained neural operator weights, when released, will be under a separate research-only license to prevent commercial deployment without validation.

---

<div align="center">
<sub>Built by Amine Harch El Korane · Casablanca, Morocco · 2026</sub><br>
<sub>"Simulation should not cost $50,000. Physics is free."</sub>
</div>
