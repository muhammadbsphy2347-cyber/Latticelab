"""
Molecular Dynamics: Simple molecular dynamics simulation
"""

import numpy as np
from typing import Tuple


class Particle:
    """
    Represents a single particle in molecular dynamics simulation.
    
    Attributes:
        position (np.ndarray): 2D position [x, y]
        velocity (np.ndarray): 2D velocity [vx, vy]
        force (np.ndarray): 2D force [fx, fy]
        mass (float): Particle mass
    """
    
    def __init__(self, position: np.ndarray, velocity: np.ndarray = None, mass: float = 1.0):
        """
        Initialize a particle.
        
        Args:
            position (np.ndarray): Initial position [x, y]
            velocity (np.ndarray, optional): Initial velocity [vx, vy]
            mass (float): Particle mass
        """
        self.position = position.astype(float)
        self.velocity = velocity if velocity is not None else np.zeros(2)
        self.force = np.zeros(2)
        self.mass = mass
    
    def update_position(self, dt: float) -> None:
        """
        Update position using velocity (Euler method).
        
        Args:
            dt (float): Time step
        """
        self.position += self.velocity * dt
    
    def update_velocity(self, dt: float) -> None:
        """
        Update velocity using acceleration (Euler method).
        
        Args:
            dt (float): Time step
        """
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
    
    def reset_force(self) -> None:
        """
        Reset force to zero.
        """
        self.force = np.zeros(2)


class MolecularDynamics:
    """
    Simple 2D Molecular Dynamics simulator.
    
    Attributes:
        particles (list): List of Particle objects
        box_size (float): Size of simulation box
        dt (float): Time step
        cutoff (float): Interaction cutoff distance
    """
    
    def __init__(self, box_size: float = 10.0, dt: float = 0.01, cutoff: float = 3.0):
        """
        Initialize MD simulator.
        
        Args:
            box_size (float): Size of cubic simulation box
            dt (float): Time step
            cutoff (float): Interaction cutoff distance
        """
        self.particles = []
        self.box_size = box_size
        self.dt = dt
        self.cutoff = cutoff
        self.energy_history = []
    
    def add_particle(self, position: np.ndarray, velocity: np.ndarray = None, mass: float = 1.0) -> None:
        """
        Add a particle to the system.
        
        Args:
            position (np.ndarray): Initial position
            velocity (np.ndarray, optional): Initial velocity
            mass (float): Particle mass
        """
        particle = Particle(position, velocity, mass)
        self.particles.append(particle)
    
    def compute_forces(self, epsilon: float = 1.0, sigma: float = 1.0) -> None:
        """
        Compute Lennard-Jones forces between all particles.
        
        Args:
            epsilon (float): Depth of potential well
            sigma (float): Finite distance at which potential is zero
        """
        # Reset forces
        for particle in self.particles:
            particle.reset_force()
        
        # Compute pairwise forces
        n = len(self.particles)
        for i in range(n):
            for j in range(i + 1, n):
                r_vec = self.particles[j].position - self.particles[i].position
                
                # Apply periodic boundary conditions
                r_vec = np.where(np.abs(r_vec) > self.box_size / 2, 
                                r_vec - np.sign(r_vec) * self.box_size, r_vec)
                
                r = np.linalg.norm(r_vec)
                
                if r < self.cutoff and r > 1e-6:
                    # Lennard-Jones force
                    factor = 24 * epsilon * (2 * (sigma ** 12) / (r ** 14) - (sigma ** 6) / (r ** 8))
                    force = factor * r_vec / r
                    
                    self.particles[i].force += force
                    self.particles[j].force -= force
    
    def calculate_kinetic_energy(self) -> float:
        """
        Calculate total kinetic energy.
        
        Returns:
            float: Kinetic energy
        """
        ke = 0.0
        for particle in self.particles:
            ke += 0.5 * particle.mass * np.sum(particle.velocity ** 2)
        return ke
    
    def simulate(self, steps: int, epsilon: float = 1.0, sigma: float = 1.0) -> None:
        """
        Run simulation for specified number of steps.
        
        Args:
            steps (int): Number of simulation steps
            epsilon (float): Lennard-Jones epsilon parameter
            sigma (float): Lennard-Jones sigma parameter
        """
        for step in range(steps):
            # Compute forces
            self.compute_forces(epsilon, sigma)
            
            # Update velocities and positions
            for particle in self.particles:
                particle.update_velocity(self.dt)
                particle.update_position(self.dt)
                
                # Periodic boundary conditions
                particle.position = np.mod(particle.position, self.box_size)
            
            # Record energy
            self.energy_history.append(self.calculate_kinetic_energy())
