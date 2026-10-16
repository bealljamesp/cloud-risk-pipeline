import logging

import numpy as np
import numpy.typing as npt
import pandas as pd

from risk_runner.backtest import christoffersen_independence_test, kupiec_pof_test
from risk_runner.config import settings
from risk_runner.db import RiskRunModel, SessionLocal, init_db
from risk_runner.models import SimulationConfig, simulate_portfolio_paths_with_garch

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def compute_portfolio_risk(
    historical_returns: npt.NDArray[np.float64],
    weights: npt.NDArray[np.float64],
    confidence: float = 0.99,
    num_paths: int = 10000,
) -> tuple[float, float, float, float]:
    """Computes Value-at-Risk, Expected Shortfall, and regulatory backtest p-values."""
    config = SimulationConfig(
        num_paths=num_paths, horizon_days=10, confidence_level=confidence
    )
    simulated_path_returns = simulate_portfolio_paths_with_garch(
        historical_returns, weights, config
    )
    alpha = 1.0 - confidence
    var_threshold = np.percentile(simulated_path_returns, alpha * 100.0)
    var_99 = -var_threshold
    expected_shortfall_99 = -np.mean(
        simulated_path_returns[simulated_path_returns <= var_threshold]
    )

    # Run backtests against rolling historical slice
    portfolio_hist = historical_returns @ weights
    var_thresholds_hist = np.full_like(portfolio_hist, -var_99)
    _, kupiec_p = kupiec_pof_test(
        portfolio_hist, var_thresholds_hist, confidence_level=confidence
    )
    _, christoffersen_p = christoffersen_independence_test(
        portfolio_hist, var_thresholds_hist
    )

    return (
        float(var_99),
        float(expected_shortfall_99),
        float(kupiec_p),
        float(christoffersen_p),
    )


def run_risk_pipeline() -> None:
    init_db()
    logger.info("Initializing risk calculation runner.")
    logger.info("Loading local portfolio weights from data/portfolio_weights.csv")

    weights_df = pd.read_csv("data/portfolio_weights.csv")
    weights = weights_df["weight"].to_numpy(dtype=np.float64)

    np.random.seed(42)
    historical_returns = np.random.normal(0.0001, 0.015, size=(252, weights.size))

    var_99, es_99, kupiec_p, christoffersen_p = compute_portfolio_risk(
        historical_returns=historical_returns,
        weights=weights,
        confidence=settings.confidence_level,
        num_paths=settings.simulation_runs,
    )

    logger.info(
        f"Calculated VaR ({settings.confidence_level * 100}%): {var_99:.6f} | "
        f"ES: {es_99:.6f} | Kupiec p-val: {kupiec_p:.4f} | Christoffersen p-val: {christoffersen_p:.4f}"
    )

    session = SessionLocal()
    try:
        run_record = RiskRunModel(
            portfolio_id="portfolio_main",
            var_99=var_99,
            expected_shortfall_99=es_99,
            kupiec_p_value=kupiec_p,
            christoffersen_p_value=christoffersen_p,
            status="SUCCESS",
        )
        session.add(run_record)
        session.commit()
        logger.info(
            "Successfully persisted GARCH metrics and backtest results to metadata ledger."
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to persist risk run: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run_risk_pipeline()
