"""
tests/test_latticelab.py
Run with:  pytest tests/ -v
"""

import math
import pytest
import numpy as np


@pytest.fixture()
def small_lattice():
    from src.lattice import SquareLattice
    return SquareLattice(size=10)

@pytest.fixture()
def ising(small_lattice):
    from src.ising_model import IsingModel
    return IsingModel(small_lattice, temperature=2.269)

@pytest.fixture()
def md_system():
    from src.molecular_dynamics import MolecularDynamics
    system = MolecularDynamics(box_size=10.0, dt=0.01)
    rng = np.random.default_rng(0)
    for _ in range(3):
        system.add_particle(rng.uniform(0, 10, 2), rng.uniform(-1, 1, 2))
    return system


class TestSquareLattice:
    def test_shape(self, small_lattice):
        assert small_lattice.grid.shape == (10, 10)

    def test_spins_binary(self, small_lattice):
        unique = set(np.unique(small_lattice.grid))
        assert unique.issubset({-1, 1})

    def test_size_attribute(self, small_lattice):
        assert small_lattice.size == 10

    def test_different_sizes(self):
        from src.lattice import SquareLattice
        for size in (4, 16, 32):
            lat = SquareLattice(size=size)
            assert lat.grid.shape == (size, size)

    def test_reproducible_with_seed(self):
        from src.lattice import SquareLattice
        lat_a = SquareLattice(size=10, seed=7)
        lat_b = SquareLattice(size=10, seed=7)
        np.testing.assert_array_equal(lat_a.grid, lat_b.grid)


class TestIsingModel:
    def test_energy_is_finite(self, ising):
        assert math.isfinite(ising.get_energy())

    def test_magnetization_range(self, ising):
        m = ising.get_magnetization()
        assert -1.0 <= m <= 1.0

    def test_simulate_runs(self, ising):
        ising.simulate(steps=50, record_interval=10)

    def test_acceptance_rate_range(self, ising):
        ising.simulate(steps=100, record_interval=10)
        assert 0.0 <= ising.get_acceptance_rate() <= 1.0

    def test_high_temp_disorder(self):
        from src.lattice import SquareLattice
        from src.ising_model import IsingModel
        model = IsingModel(SquareLattice(size=20, seed=0), temperature=100.0)
        model.simulate(steps=2000, record_interval=100)
        assert abs(model.get_magnetization()) < 0.5

    def test_low_temp_order(self):
        from src.lattice import SquareLattice
        from src.ising_model import IsingModel
        model = IsingModel(SquareLattice(size=20, seed=0), temperature=0.1)
        model.simulate(steps=2000, record_interval=100)
        assert abs(model.get_magnetization()) > 0.5


class TestMolecularDynamics:
    def test_particle_count(self, md_system):
        assert md_system.n_particles == 3

    def test_simulate_runs(self, md_system):
        md_system.simulate(steps=50)

    def test_energy_history_populated(self, md_system):
        md_system.simulate(steps=50)
        assert len(md_system.energy_history) > 0

    def test_energy_is_finite(self, md_system):
        md_system.simulate(steps=100)
        assert all(math.isfinite(e) for e in md_system.energy_history)

    def test_energy_non_negative(self, md_system):
        md_system.simulate(steps=100)
        assert all(e >= 0 for e in md_system.energy_history)

    def test_add_particle_increases_count(self):
        from src.molecular_dynamics import MolecularDynamics
        md = MolecularDynamics(box_size=5.0, dt=0.01)
        assert md.n_particles == 0
        md.add_particle(np.array([1.0, 1.0]), np.array([0.0, 0.0]))
        assert md.n_particles == 1


class TestUtils:
    def test_calculate_statistics_mean(self):
        from src.utils import calculate_statistics
        stats = calculate_statistics([1.0, 2.0, 3.0, 4.0, 5.0])
        assert math.isclose(stats["mean"], 3.0)

    def test_calculate_statistics_std(self):
        from src.utils import calculate_statistics
        data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        stats = calculate_statistics(data)
        assert math.isclose(stats["std"], np.std(data), rel_tol=1e-6)

    def test_plot_observables_returns(self):
        import matplotlib
        matplotlib.use("Agg")
        from src.utils import plot_observables
        plot_observables(list(range(10)), title="Test")
