import numpy as np

from risk_runner.backtest import christoffersen_independence_test, kupiec_pof_test


def test_kupiec_pof_test() -> None:
    np.random.seed(42)
    returns = np.random.normal(0.0, 0.01, size=250)
    var_thresholds = np.full(250, -0.023)

    lr_stat, p_val = kupiec_pof_test(returns, var_thresholds, confidence_level=0.99)

    assert isinstance(lr_stat, float)
    assert isinstance(p_val, float)
    assert 0.0 <= p_val <= 1.0


def test_christoffersen_independence_test() -> None:
    np.random.seed(42)
    returns = np.random.normal(0.0, 0.01, size=250)
    var_thresholds = np.full(250, -0.023)

    lr_stat, p_val = christoffersen_independence_test(returns, var_thresholds)

    assert isinstance(lr_stat, float)
    assert isinstance(p_val, float)
    assert 0.0 <= p_val <= 1.0
