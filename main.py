#!/usr/bin/env python3
"""
Latticelab: Main entry point for physics simulations
"""

from src.lattice import SquareLattice
from src.ising_model import IsingModel
from src.molecular_dynamics import MolecularDynamics
from src.utils import calculate_statistics, plot_observables
import numpy as np


def main():
    """
    Main function to run default simulations.
    """
    print("Welcome to Latticelab!")
    print("Computational Physics Simulations\n")
    
    # Example 1: Ising Model Simulation
    print("=" * 50)
    print("Running Ising Model Simulation...")
    print("=" * 50)
    
    lattice = SquareLattice(size=32)
    ising = IsingModel(lattice, temperature=2.0)
    ising.simulate(steps=1000, record_interval=1)
    
    print(f"\nFinal Energy: {ising.get_energy():.4f}")
    print(f"Final Magnetization: {ising.get_magnetization():.4f}")
    print(f"Acceptance Rate: {ising.get_acceptance_rate():.4f}")
    
    # Example 2: Molecular Dynamics Simulation
    print("\n" + "=" * 50)
    print("Running Molecular Dynamics Simulation...")
    print("=" * 50)
    
    md = MolecularDynamics(box_size=10.0, dt=0.01)
    
    # Add particles
    np.random.seed(42)
    for _ in range(5):
        pos = np.random.uniform(0, 10, 2)
        vel = np.random.uniform(-1, 1, 2)
        md.add_particle(pos, vel)
    
    md.simulate(steps=500)
    
    print(f"Final Kinetic Energy: {md.energy_history[-1]:.4f}")
    print(f"Average Kinetic Energy: {np.mean(md.energy_history):.4f}")
    
    print("\n" + "=" * 50)
    print("Simulations completed!")
    print("See examples/simulation_example.py for more examples.")
    print("=" * 50)


if __name__ == "__main__":
    main()
