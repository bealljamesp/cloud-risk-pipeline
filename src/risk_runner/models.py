from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(slots=True, frozen=True)
class SimulationConfig:
    num_paths: int = 10000
    horizon_days: int = 10
    confidence_level: float = 0.99


def simulate_portfolio_paths(
    mean_returns: npt.NDArray[np.float64],
    covariance_matrix: npt.NDArray[np.float64],
    weights: npt.NDArray[np.float64],
    config: SimulationConfig,
) -> npt.NDArray[np.float64]:
    """Generates multi-period correlated asset paths via Cholesky decomposition.

    Adheres strictly to vectorized NumPy operations without explicit loops.
    """
    num_assets = weights.size
    cholesky_factor = np.linalg.cholesky(covariance_matrix)

    # Standard normal shocks: shape (num_paths, horizon_days, num_assets)
    random_shocks = np.random.standard_normal(
        size=(config.num_paths, config.horizon_days, num_assets)
    )

    # Correlated asset returns across paths and time steps
    correlated_shocks = random_shocks @ cholesky_factor.T
    path_returns = mean_returns + correlated_shocks

    # Aggregate to portfolio level over the horizon: shape (num_paths, horizon_days)
    portfolio_path_values = path_returns @ weights
    cumulative_path_returns = np.sum(portfolio_path_values, axis=1)

    return cumulative_path_returns
