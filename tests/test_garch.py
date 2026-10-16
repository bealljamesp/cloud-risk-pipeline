import numpy as np

from risk_runner.garch import compute_gjr_garch_volatility


def test_gjr_garch_asymmetry() -> None:
    # Construct synthetic returns with a large negative shock
    returns = np.array([0.01, -0.05, 0.005, -0.002, 0.01], dtype=np.float64)
    volatilities = compute_gjr_garch_volatility(returns)

    assert volatilities.shape == returns.shape
    assert not np.isnan(volatilities).any()
    # Volatility should spike following the large negative shock at index 1
    assert volatilities[2] > volatilities[0]
