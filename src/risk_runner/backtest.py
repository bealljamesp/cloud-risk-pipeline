import numpy as np
import numpy.typing as npt
from scipy.stats import chi2


def kupiec_pof_test(
    returns: npt.NDArray[np.float64],
    var_thresholds: npt.NDArray[np.float64],
    confidence_level: float = 0.99,
) -> tuple[float, float]:
    """Performs Kupiec Proportion of Failures (POF) test on VaR exceptions."""
    failures = np.sum(returns < var_thresholds)
    total_observations = returns.size
    failure_rate = failures / total_observations
    target_rate = 1.0 - confidence_level

    if failures == 0:
        lr_statistic = -2.0 * np.log((1.0 - target_rate) ** total_observations)
    else:
        term1 = (total_observations - failures) * np.log(1.0 - target_rate)
        term2 = failures * np.log(target_rate)
        term3 = (total_observations - failures) * np.log(1.0 - failure_rate)
        term4 = failures * np.log(failure_rate)
        lr_statistic = -2.0 * ((term1 + term2) - (term3 + term4))

    p_value = 1.0 - chi2.cdf(lr_statistic, df=1)
    return float(lr_statistic), float(p_value)


def christoffersen_independence_test(
    returns: npt.NDArray[np.float64], var_thresholds: npt.NDArray[np.float64]
) -> tuple[float, float]:
    """Performs Christoffersen Markov chain independence test on VaR exceptions.

    Returns the likelihood ratio test statistic and p-value for independence.
    """
    exceptions = (returns < var_thresholds).astype(int)

    # Transition matrix counts: N_ij where i is state at t-1, j is state at t
    n00 = np.sum((exceptions[:-1] == 0) & (exceptions[1:] == 0))
    n01 = np.sum((exceptions[:-1] == 0) & (exceptions[1:] == 1))
    n10 = np.sum((exceptions[:-1] == 1) & (exceptions[1:] == 0))
    n11 = np.sum((exceptions[:-1] == 1) & (exceptions[1:] == 1))

    pi_0 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0.0
    pi_1 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0.0
    pi = (n01 + n11) / (n00 + n01 + n10 + n11) if (n00 + n01 + n10 + n11) > 0 else 0.0

    # Avoid log(0) errors
    def safe_log(x: float) -> float:
        return np.log(x) if x > 0.0 else 0.0

    l0 = (n00 + n10) * safe_log(1.0 - pi) + (n01 + n11) * safe_log(pi)
    l1 = (
        n00 * safe_log(1.0 - pi_0)
        + n01 * safe_log(pi_0)
        + n10 * safe_log(1.0 - pi_1)
        + n11 * safe_log(pi_1)
    )

    lr_stat = -2.0 * (l0 - l1)
    p_val = 1.0 - chi2.cdf(lr_stat, df=1)

    return float(lr_stat), float(p_val)
