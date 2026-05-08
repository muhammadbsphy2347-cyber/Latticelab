"""
Tests for SquareLattice module.
"""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lattice import SquareLattice


def test_lattice_creation():
    """Test that a lattice is created with correct size."""
    lattice = SquareLattice(size=10)
    assert lattice is not None


def test_lattice_shape():
    """Test that lattice grid has correct dimensions."""
    size = 10
    lattice = SquareLattice(size=size)
    assert lattice.grid.shape == (size, size)


def test_lattice_values():
    """Test that lattice values are either +1 or -1 (spin values)."""
    lattice = SquareLattice(size=20)
    unique_values = np.unique(lattice.grid)
    for val in unique_values:
        assert val in [-1, 1], f"Unexpected spin value: {val}"


def test_lattice_size_attribute():
    """Test that lattice stores correct size attribute."""
    lattice = SquareLattice(size=15)
    assert lattice.size == 15
