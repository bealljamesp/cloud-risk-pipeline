from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from risk_runner.garch import compute_gjr_garch_volatility


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
    """Generates multi-period correlated asset paths via Cholesky decomposition."""
    num_assets = weights.size
    cholesky_factor = np.linalg.cholesky(covariance_matrix)

    random_shocks = np.random.standard_normal(
        size=(config.num_paths, config.horizon_days, num_assets)
    )
    correlated_shocks = random_shocks @ cholesky_factor.T
    path_returns = mean_returns + correlated_shocks
    portfolio_path_values = path_returns @ weights
    cumulative_path_returns = np.sum(portfolio_path_values, axis=1)

    return cumulative_path_returns


def simulate_portfolio_paths_with_garch(
    historical_returns: npt.NDArray[np.float64],
    weights: npt.NDArray[np.float64],
    config: SimulationConfig,
) -> npt.NDArray[np.float64]:
    """Generates portfolio path returns scaled by GJR-GARCH conditional volatility."""
    portfolio_historical_returns = historical_returns @ weights
    conditional_vol = compute_gjr_garch_volatility(portfolio_historical_returns)
    latest_vol = conditional_vol[-1]

    random_shocks = np.random.standard_normal(
        size=(config.num_paths, config.horizon_days)
    )
    scaled_paths = random_shocks * latest_vol
    cumulative_path_returns = np.sum(scaled_paths, axis=1)

    return cumulative_path_returns
