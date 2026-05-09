# Latticelab

[![CI](https://github.com/muhammadbsphy2347-cyber/Latticelab/actions/workflows/ci.yml/badge.svg)](https://github.com/muhammadbsphy2347-cyber/Latticelab/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%20|%203.11%20|%203.12-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python toolkit for **computational physics simulations** and **data modelling**, focused on accuracy, efficiency, and clear documentation.

---

## Table of Contents

- [Overview](#overview)
- [Physics Background](#physics-background)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Latticelab provides a suite of Python tools for simulating lattice-based physical systems:

- **2D Square Lattice** – configurable spin lattice with periodic boundary conditions
- **Ising Model** – Metropolis Monte Carlo algorithm for studying magnetic phase transitions
- **Molecular Dynamics** – velocity-Verlet integration for particle dynamics
- **Analysis utilities** – statistical analysis and plotting helpers

---

## Physics Background

### Ising Model

The Ising model describes a lattice of magnetic spins (±1) interacting with their nearest neighbours. At the critical temperature Tc ≈ 2.269 J/kB (2D square lattice), the system undergoes a phase transition from ferromagnetic (ordered) to paramagnetic (disordered). Latticelab uses the Metropolis algorithm to sample configurations from the Boltzmann distribution.

### Molecular Dynamics

The MD module integrates Newton's equations of motion using the velocity-Verlet algorithm. Particle interactions are modelled with a Lennard-Jones potential between each pair of particles.

---

## Project Structure                                                                                                          Latticelab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── examples/
│   └── simulation_example.py
├── src/
│   ├── lattice.py
│   ├── ising_model.py
│   ├── molecular_dynamics.py
│   └── utils.py
├── tests/
│   └── test_latticelab.py
├── conftest.py
├── main.py
├── pytest.ini
├── ruff.toml
├── requirements.txt
└── README.md
---

## Installation

```bash
git clone https://github.com/muhammadbsphy2347-cyber/Latticelab.git
cd Latticelab
pip install -r requirements.txt
```

Requires **Python 3.9+**.

---

## Usage

### Run all simulations with defaults

```bash
python main.py
```

### Run only the Ising model

```bash
python main.py --sim ising
```

### Run only Molecular Dynamics

```bash
python main.py --sim md
```

### Custom parameters

```bash
python main.py --sim ising --size 64 --temp 2.269 --steps 5000
python main.py --sim md --n-particles 20 --dt 0.005 --md-steps 2000
python main.py -v
```

### Use the API directly

```python
from src.lattice import SquareLattice
from src.ising_model import IsingModel

lattice = SquareLattice(size=50, seed=0)
ising = IsingModel(lattice, temperature=2.269)
ising.simulate(steps=5000, record_interval=50)

print(f"Magnetization : {ising.get_magnetization():.4f}")
print(f"Energy        : {ising.get_energy():.4f}")
```

---

## Running Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Example Output                                                                                                             13:45:01 [INFO] Welcome to Latticelab - Computational Physics Simulations
13:45:01 [INFO] ==================================================
13:45:01 [INFO] Running Ising Model Simulation
13:45:01 [INFO]   Lattice size : 32 x 32
13:45:01 [INFO]   Temperature  : 2.0000
13:45:01 [INFO]   Steps        : 1000
13:45:01 [INFO] ==================================================
13:45:02 [INFO] Final Energy        : -1.7823
13:45:02 [INFO] Final Magnetization : 0.8341
13:45:02 [INFO] Acceptance Rate     : 0.2156                                                                                  ---

## Contributing

1. Fork the repo and create a feature branch (`git checkout -b feature/my-feature`)
2. Make your changes and add tests in `tests/`
3. Ensure all tests pass (`pytest tests/ -v`)
4. Open a pull request with a clear description

---

## License

This project is licensed under the [MIT License](LICENSE).
