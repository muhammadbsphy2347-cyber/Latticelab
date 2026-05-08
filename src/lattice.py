"""
Lattice Module: Base classes for lattice structures
"""

import numpy as np
from typing import Tuple, Optional


class SquareLattice:
    """
    2D Square Lattice implementation for physics simulations.
    
    Attributes:
        size (int): Dimension of the square lattice (size x size)
        grid (np.ndarray): 2D array representing the lattice spin values
    """
    
    def __init__(self, size: int, initial_state: Optional[np.ndarray] = None):
        """
        Initialize a square lattice.
        
        Args:
            size (int): Dimension of the lattice
            initial_state (np.ndarray, optional): Initial spin configuration
        """
        self.size = size
        
        if initial_state is not None:
            self.grid = initial_state.copy()
        else:
            # Random initialization with spins +1 or -1
            self.grid = np.random.choice([1, -1], size=(size, size))
    
    def get_spin(self, i: int, j: int) -> int:
        """
        Get spin value at position (i, j) with periodic boundary conditions.
        
        Args:
            i (int): Row index
            j (int): Column index
            
        Returns:
            int: Spin value (+1 or -1)
        """
        return self.grid[i % self.size, j % self.size]
    
    def set_spin(self, i: int, j: int, value: int) -> None:
        """
        Set spin value at position (i, j).
        
        Args:
            i (int): Row index
            j (int): Column index
            value (int): Spin value (+1 or -1)
        """
        self.grid[i % self.size, j % self.size] = value
    
    def get_neighbors(self, i: int, j: int) -> list:
        """
        Get spin values of four nearest neighbors (up, down, left, right).
        
        Args:
            i (int): Row index
            j (int): Column index
            
        Returns:
            list: Spin values of neighbors
        """
        neighbors = [
            self.get_spin(i+1, j),  # down
            self.get_spin(i-1, j),  # up
            self.get_spin(i, j+1),  # right
            self.get_spin(i, j-1)   # left
        ]
        return neighbors
    
    def flip_spin(self, i: int, j: int) -> None:
        """
        Flip the spin at position (i, j).
        
        Args:
            i (int): Row index
            j (int): Column index
        """
        self.grid[i, j] *= -1
    
    def reset(self, random: bool = True) -> None:
        """
        Reset the lattice to a new configuration.
        
        Args:
            random (bool): If True, random configuration; if False, all +1
        """
        if random:
            self.grid = np.random.choice([1, -1], size=(self.size, self.size))
        else:
            self.grid = np.ones((self.size, self.size), dtype=int)
    
    def copy(self) -> 'SquareLattice':
        """
        Create a deep copy of the lattice.
        
        Returns:
            SquareLattice: Copy of the current lattice
        """
        return SquareLattice(self.size, self.grid.copy())
