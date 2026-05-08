"""
Utility functions for analysis and visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple


def calculate_statistics(data: List[float]) -> dict:
    """
    Calculate basic statistics for a data series.
    
    Args:
        data (List[float]): Data series
        
    Returns:
        dict: Dictionary containing mean, std, min, max
    """
    data_array = np.array(data)
    return {
        'mean': np.mean(data_array),
        'std': np.std(data_array),
        'min': np.min(data_array),
        'max': np.max(data_array),
        'median': np.median(data_array)
    }


def plot_lattice(lattice) -> None:
    """
    Plot 2D lattice spin configuration.
    
    Args:
        lattice: SquareLattice object
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(lattice.grid, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label='Spin')
    plt.title('Lattice Configuration')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


def plot_observables(energy: List[float], magnetization: List[float]) -> None:
    """
    Plot energy and magnetization vs time steps.
    
    Args:
        energy (List[float]): Energy history
        magnetization (List[float]): Magnetization history
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    steps = np.arange(len(energy))
    
    ax1.plot(steps, energy, 'b-', linewidth=0.7)
    ax1.set_xlabel('MC Steps')
    ax1.set_ylabel('Energy')
    ax1.set_title('Energy Evolution')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(steps, magnetization, 'r-', linewidth=0.7)
    ax2.set_xlabel('MC Steps')
    ax2.set_ylabel('Magnetization')
    ax2.set_title('Magnetization Evolution')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def plot_phase_diagram(temperatures: List[float], magnetizations: List[float]) -> None:
    """
    Plot phase diagram (Magnetization vs Temperature).
    
    Args:
        temperatures (List[float]): Temperature values
        magnetizations (List[float]): Corresponding magnetizations
    """
    plt.figure(figsize=(10, 6))
    plt.plot(temperatures, magnetizations, 'o-', linewidth=2, markersize=8)
    plt.axvline(x=2.269, color='r', linestyle='--', label='Critical T (Theory)')
    plt.xlabel('Temperature (T/J)')
    plt.ylabel('Magnetization')
    plt.title('Phase Diagram: 2D Ising Model')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def save_data(filename: str, data: dict) -> None:
    """
    Save simulation data to file.
    
    Args:
        filename (str): Output filename
        data (dict): Data dictionary to save
    """
    np.save(filename, data)
    print(f"Data saved to {filename}")


def load_data(filename: str) -> dict:
    """
    Load simulation data from file.
    
    Args:
        filename (str): Input filename
        
    Returns:
        dict: Loaded data
    """
    data = np.load(filename, allow_pickle=True).item()
    print(f"Data loaded from {filename}")
    return data
