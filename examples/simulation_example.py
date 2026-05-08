"""
Example: Running Ising Model Simulations
"""

import sys
sys.path.insert(0, '../')

from src.lattice import SquareLattice
from src.ising_model import IsingModel
from src.utils import calculate_statistics, plot_observables
import numpy as np


def example_single_temperature():
    """
    Run a single Ising model simulation at fixed temperature.
    """
    print("=" * 50)
    print("Example 1: Single Temperature Simulation")
    print("=" * 50)
    
    # Create lattice
    lattice_size = 32
    lattice = SquareLattice(size=lattice_size)
    
    # Create Ising model
    temperature = 2.0
    ising = IsingModel(lattice, temperature=temperature)
    
    # Run simulation
    print(f"Simulating {lattice_size}x{lattice_size} lattice at T = {temperature}")
    ising.simulate(steps=5000, record_interval=10)
    
    # Print statistics
    energy_stats = calculate_statistics(ising.energy_history)
    mag_stats = calculate_statistics(ising.magnetization_history)
    
    print(f"\nEnergy Statistics:")
    print(f"  Mean: {energy_stats['mean']:.4f}")
    print(f"  Std:  {energy_stats['std']:.4f}")
    print(f"  Min:  {energy_stats['min']:.4f}")
    print(f"  Max:  {energy_stats['max']:.4f}")
    
    print(f"\nMagnetization Statistics:")
    print(f"  Mean: {mag_stats['mean']:.4f}")
    print(f"  Std:  {mag_stats['std']:.4f}")
    print(f"  Min:  {mag_stats['min']:.4f}")
    print(f"  Max:  {mag_stats['max']:.4f}")
    
    print(f"\nAcceptance Rate: {ising.get_acceptance_rate():.4f}")
    
    return ising


def example_phase_transition():
    """
    Study phase transition by varying temperature.
    """
    print("\n" + "=" * 50)
    print("Example 2: Phase Transition Study")
    print("=" * 50)
    
    lattice_size = 32
    temperatures = np.linspace(0.5, 4.0, 8)
    magnetizations = []
    
    print(f"Scanning temperatures from {temperatures[0]} to {temperatures[-1]}\n")
    
    for i, T in enumerate(temperatures):
        # Create fresh lattice
        lattice = SquareLattice(size=lattice_size)
        ising = IsingModel(lattice, temperature=T)
        
        # Run simulation
        ising.simulate(steps=2000, record_interval=10)
        
        # Extract final magnetization
        mag = ising.get_magnetization()
        magnetizations.append(mag)
        
        print(f"T = {T:.2f}: M = {mag:.4f}")
    
    print(f"\nPhase transition observed around T ≈ 2.269 (theoretical)")
    return temperatures, magnetizations


if __name__ == "__main__":
    # Run examples
    ising_model = example_single_temperature()
    temps, mags = example_phase_transition()
    
    print("\n" + "=" * 50)
    print("Examples completed successfully!")
    print("=" * 50)
