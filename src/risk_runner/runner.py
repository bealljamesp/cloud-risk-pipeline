import logging
from io import StringIO

import boto3
import numpy as np
import numpy.typing as npt
import pandas as pd

from risk_runner.config import settings
from risk_runner.db import RiskRunModel, SessionLocal

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def compute_portfolio_risk(
    returns: npt.NDArray[np.float64],
    weights: npt.NDArray[np.float64],
    confidence: float = 0.99,
) -> tuple[float, float]:
    """Computes Parametric VaR and Expected Shortfall using vectorized NumPy operations."""
    portfolio_returns: npt.NDArray[np.float64] = returns @ weights
    mean_ret = np.mean(portfolio_returns)
    std_ret = np.std(portfolio_returns, ddof=1)

    # Parametric VaR using normal approximation (or historical quantile)
    var_val = float(np.percentile(portfolio_returns, (1.0 - confidence) * 100.0))

    # Expected Shortfall (Conditional VaR)
    tail_losses = portfolio_returns[portfolio_returns <= var_val]
    es_val = float(np.mean(tail_losses)) if tail_losses.size > 0 else var_val

    return abs(var_val), abs(es_val)


def main() -> None:
    logger.info("Initializing serverless risk calculation runner.")
    s3_client = boto3.client("s3", region_name=settings.aws_region)

    logger.info(
        f"Fetching portfolio payload from s3://{settings.s3_bucket_name}/{settings.portfolio_file_key}"
    )
    obj = s3_client.get_object(
        Bucket=settings.s3_bucket_name, Key=settings.portfolio_file_key
    )
    csv_data = obj["Body"].read().decode("utf-8")

    df = pd.read_csv(filepath_or_buffer=StringIO(csv_data))

    # Expecting columns: asset_id, weight, and historical return series
    weights: npt.NDArray[np.float64] = df["weight"].to_numpy(
        dtype=np.float64, copy=False
    )
    return_cols = [c for c in df.columns if c.startswith("ret_")]
    returns_matrix: npt.NDArray[np.float64] = (
        df[return_cols].to_numpy(dtype=np.float64, copy=False).T
    )

    var_99, es_99 = compute_portfolio_risk(
        returns_matrix, weights, confidence=settings.confidence_level
    )
    logger.info(
        f"Calculated VaR ({settings.confidence_level * 100}%): {var_99:.6f} | ES: {es_99:.6f}"
    )

    session = SessionLocal()
    try:
        run_record = RiskRunModel(
            portfolio_id="PRIMARY_BOOK",
            var_99=var_99,
            expected_shortfall_99=es_99,
            status="SUCCESS",
        )
        session.add(run_record)
        session.commit()
        logger.info(
            "Successfully persisted risk metrics to PostgreSQL metadata ledger."
        )
    except Exception as exc:
        session.rollback()
        logger.error(f"Failed to commit risk metrics to database: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
