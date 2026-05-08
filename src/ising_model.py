"""
Ising Model: Classical 2D Ising model implementation
"""

import numpy as np
from src.lattice import SquareLattice
from typing import List


class IsingModel:
    """
    2D Ising Model simulator using Metropolis algorithm.
    
    Attributes:
        lattice (SquareLattice): The spin lattice
        temperature (float): Temperature parameter (T)
        J (float): Coupling constant
        energy_history (list): Energy at each step
        magnetization_history (list): Magnetization at each step
    """
    
    def __init__(self, lattice: SquareLattice, temperature: float = 1.0, J: float = 1.0):
        """
        Initialize the Ising model.
        
        Args:
            lattice (SquareLattice): Initial lattice configuration
            temperature (float): Temperature parameter
            J (float): Coupling constant
        """
        self.lattice = lattice
        self.temperature = temperature
        self.J = J
        self.energy_history = []
        self.magnetization_history = []
        self.acceptance_rate = 0
    
    def calculate_energy(self) -> float:
        """
        Calculate total energy of the system.
        
        Returns:
            float: Total energy
        """
        energy = 0.0
        for i in range(self.lattice.size):
            for j in range(self.lattice.size):
                spin = self.lattice.get_spin(i, j)
                neighbors = self.lattice.get_neighbors(i, j)
                energy -= self.J * spin * sum(neighbors)
        return energy / 2.0  # Avoid double counting
    
    def calculate_magnetization(self) -> float:
        """
        Calculate magnetization of the system.
        
        Returns:
            float: Average magnetization per spin
        """
        total_spin = np.sum(self.lattice.grid)
        return abs(total_spin) / (self.lattice.size ** 2)
    
    def energy_change(self, i: int, j: int) -> float:
        """
        Calculate energy change if spin at (i, j) is flipped.
        
        Args:
            i (int): Row index
            j (int): Column index
            
        Returns:
            float: Energy change
        """
        spin = self.lattice.get_spin(i, j)
        neighbors = self.lattice.get_neighbors(i, j)
        dE = 2 * self.J * spin * sum(neighbors)
        return dE
    
    def metropolis_step(self) -> bool:
        """
        Perform one Metropolis algorithm step.
        
        Returns:
            bool: True if spin flip was accepted
        """
        i = np.random.randint(0, self.lattice.size)
        j = np.random.randint(0, self.lattice.size)
        
        dE = self.energy_change(i, j)
        
        # Metropolis acceptance criterion
        if dE < 0 or np.random.random() < np.exp(-dE / self.temperature):
            self.lattice.flip_spin(i, j)
            return True
        return False
    
    def simulate(self, steps: int, record_interval: int = 1) -> None:
        """
        Run simulation for specified number of steps.
        
        Args:
            steps (int): Number of Monte Carlo steps
            record_interval (int): Record observables every N steps
        """
        accepted = 0
        
        for step in range(steps):
            if self.metropolis_step():
                accepted += 1
            
            if (step + 1) % record_interval == 0:
                self.energy_history.append(self.calculate_energy())
                self.magnetization_history.append(self.calculate_magnetization())
        
        self.acceptance_rate = accepted / steps
    
    def get_energy(self) -> float:
        """
        Get current total energy.
        
        Returns:
            float: Total energy
        """
        return self.calculate_energy()
    
    def get_magnetization(self) -> float:
        """
        Get current magnetization.
        
        Returns:
            float: Magnetization
        """
        return self.calculate_magnetization()
    
    def get_acceptance_rate(self) -> float:
        """
        Get acceptance rate of last simulation.
        
        Returns:
            float: Acceptance rate (0 to 1)
        """
        return self.acceptance_rate
