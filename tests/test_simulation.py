import numpy as np

from risk_runner.models import (
    SimulationConfig,
    simulate_portfolio_paths,
    simulate_portfolio_paths_with_garch,
)


def test_simulation_pipeline() -> None:
    mean_returns = np.array([0.0001, 0.0002], dtype=np.float64)
    cov_matrix = np.array([[0.0004, 0.0001], [0.0001, 0.0009]], dtype=np.float64)
    weights = np.array([0.5, 0.5], dtype=np.float64)
    config = SimulationConfig(num_paths=1000, horizon_days=5)

    paths = simulate_portfolio_paths(mean_returns, cov_matrix, weights, config)

    assert paths.shape == (1000,)
    assert not np.isnan(paths).any()


def test_garch_simulation_pipeline() -> None:
    returns = np.random.normal(0.0001, 0.01, size=(100, 2))
    weights = np.array([0.6, 0.4], dtype=np.float64)
    config = SimulationConfig(num_paths=1000, horizon_days=5)

    paths = simulate_portfolio_paths_with_garch(returns, weights, config)

    assert paths.shape == (1000,)
    assert not np.isnan(paths).any()
