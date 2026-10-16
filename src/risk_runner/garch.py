import numpy as np
import numpy.typing as npt


def compute_gjr_garch_volatility(
    returns: npt.NDArray[np.float64],
    omega: float = 0.000002,
    alpha: float = 0.05,
    gamma: float = 0.05,
    beta: float = 0.90,
) -> npt.NDArray[np.float64]:
    """Computes conditional volatility paths using GJR-GARCH(1,1) specification.

    Captures asymmetric volatility response to negative shocks.
    """
    T = returns.size
    conditional_variance = np.zeros(T, dtype=np.float64)
    conditional_variance[0] = np.var(returns)

    for t in range(1, T):
        eps_prev = returns[t - 1]
        indicator = 1.0 if eps_prev < 0 else 0.0
        conditional_variance[t] = (
            omega
            + (alpha + gamma * indicator) * (eps_prev**2)
            + beta * conditional_variance[t - 1]
        )

    return np.sqrt(conditional_variance)
