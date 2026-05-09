#!/usr/bin/env python3
"""
Latticelab: Main entry point for physics simulations.

Usage:
    python main.py                          # run all simulations with defaults
    python main.py --sim ising              # run only the Ising model
    python main.py --sim md                 # run only Molecular Dynamics
    python main.py --size 64 --temp 2.269  # custom lattice size and temperature
    python main.py --steps 5000 --seed 0   # custom steps and RNG seed
"""

import argparse
import logging
import sys

import numpy as np

# ---------------------------------------------------------------------------
# Named constants
# ---------------------------------------------------------------------------
DEFAULT_LATTICE_SIZE = 32
DEFAULT_TEMPERATURE = 2.0
DEFAULT_ISING_STEPS = 1000
DEFAULT_ISING_RECORD_INTERVAL = 10

DEFAULT_BOX_SIZE = 10.0
DEFAULT_DT = 0.01
DEFAULT_N_PARTICLES = 5
DEFAULT_MD_STEPS = 500
DEFAULT_MD_SEED = 42

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Simulation runners
# ---------------------------------------------------------------------------

def run_ising(size: int, temperature: float, steps: int, record_interval: int) -> None:
    """Run the Ising model simulation and print summary statistics."""
    try:
        from src.lattice import SquareLattice
        from src.ising_model import IsingModel
    except ImportError as exc:
        logger.error("Could not import Ising model modules: %s", exc)
        logger.error("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

    logger.info("=" * 50)
    logger.info("Running Ising Model Simulation")
    logger.info("  Lattice size : %d x %d", size, size)
    logger.info("  Temperature  : %.4f", temperature)
    logger.info("  Steps        : %d", steps)
    logger.info("=" * 50)

    lattice = SquareLattice(size=size)
    ising = IsingModel(lattice, temperature=temperature)
    ising.simulate(steps=steps, record_interval=record_interval)

    logger.info("Final Energy        : %.4f", ising.get_energy())
    logger.info("Final Magnetization : %.4f", ising.get_magnetization())
    logger.info("Acceptance Rate     : %.4f", ising.get_acceptance_rate())


def run_md(
    box_size: float,
    dt: float,
    n_particles: int,
    steps: int,
    seed: int,
) -> None:
    """Run the Molecular Dynamics simulation and print summary statistics."""
    try:
        from src.molecular_dynamics import MolecularDynamics
    except ImportError as exc:
        logger.error("Could not import Molecular Dynamics module: %s", exc)
        logger.error("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

    logger.info("=" * 50)
    logger.info("Running Molecular Dynamics Simulation")
    logger.info("  Box size    : %.2f", box_size)
    logger.info("  Time step   : %.4f", dt)
    logger.info("  Particles   : %d", n_particles)
    logger.info("  Steps       : %d", steps)
    logger.info("  RNG seed    : %d", seed)
    logger.info("=" * 50)

    md = MolecularDynamics(box_size=box_size, dt=dt)

    rng = np.random.default_rng(seed)
    for _ in range(n_particles):
        pos = rng.uniform(0, box_size, 2)
        vel = rng.uniform(-1, 1, 2)
        md.add_particle(pos, vel)

    md.simulate(steps=steps)

    logger.info("Final Kinetic Energy   : %.4f", md.energy_history[-1])
    logger.info("Average Kinetic Energy : %.4f", np.mean(md.energy_history))


# ---------------------------------------------------------------------------
# CLI argument parser
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Latticelab - computational physics simulations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--sim",
        choices=["ising", "md", "all"],
        default="all",
        help="Which simulation to run.",
    )

    ising_group = parser.add_argument_group("Ising Model")
    ising_group.add_argument("--size", type=int, default=DEFAULT_LATTICE_SIZE,
                             help="Lattice side length (NxN).")
    ising_group.add_argument("--temp", type=float, default=DEFAULT_TEMPERATURE,
                             help="Simulation temperature (kT/J).")
    ising_group.add_argument("--steps", type=int, default=DEFAULT_ISING_STEPS,
                             help="Number of Monte Carlo steps.")
    ising_group.add_argument("--record-interval", type=int,
                             default=DEFAULT_ISING_RECORD_INTERVAL,
                             help="Record observables every N steps.")

    md_group = parser.add_argument_group("Molecular Dynamics")
    md_group.add_argument("--box-size", type=float, default=DEFAULT_BOX_SIZE,
                          help="Simulation box side length.")
    md_group.add_argument("--dt", type=float, default=DEFAULT_DT,
                          help="Integration time step.")
    md_group.add_argument("--n-particles", type=int, default=DEFAULT_N_PARTICLES,
                          help="Number of particles.")
    md_group.add_argument("--md-steps", type=int, default=DEFAULT_MD_STEPS,
                          help="Number of MD integration steps.")
    md_group.add_argument("--seed", type=int, default=DEFAULT_MD_SEED,
                          help="Random seed for particle initialisation.")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable DEBUG-level logging.")

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Welcome to Latticelab - Computational Physics Simulations")

    if args.sim in ("ising", "all"):
        run_ising(
            size=args.size,
            temperature=args.temp,
            steps=args.steps,
            record_interval=args.record_interval,
        )

    if args.sim in ("md", "all"):
        run_md(
            box_size=args.box_size,
            dt=args.dt,
            n_particles=args.n_particles,
            steps=args.md_steps,
            seed=args.seed,
        )

    logger.info("=" * 50)
    logger.info("All simulations completed.")
    logger.info("See examples/simulation_example.py for more usage examples.")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
