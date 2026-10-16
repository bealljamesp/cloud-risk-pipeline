import numpy as np
import numpy.typing as npt

from risk_runner.runner import compute_portfolio_risk


def test_compute_portfolio_risk_shapes_and_bounds() -> None:
    np.random.seed(42)
    returns: npt.NDArray[np.float64] = np.random.normal(0.0005, 0.02, size=(252, 5))
    weights: npt.NDArray[np.float64] = np.array(
        [0.2, 0.2, 0.2, 0.2, 0.2], dtype=np.float64
    )

    var, es = compute_portfolio_risk(returns, weights, confidence=0.99)

    assert isinstance(var, float)
    assert isinstance(es, float)
    assert var >= 0.0
    assert es >= var
