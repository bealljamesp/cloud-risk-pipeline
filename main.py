import logging

from risk_runner.db import RiskRunModel, SessionLocal
from risk_runner.runner import run_risk_pipeline

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting local quantitative risk pipeline execution.")
    run_risk_pipeline()

    session = SessionLocal()
    try:
        runs = (
            session.query(RiskRunModel)
            .order_by(RiskRunModel.run_timestamp.desc())
            .limit(5)
            .all()
        )
        if not runs:
            logger.info("No risk runs found in metadata ledger.")
            return

        print("\n" + "=" * 80)
        print(
            f"{'ID':<4} | {'TIMESTAMP (UTC)':<20} | {'PORTFOLIO':<15} | {'VaR 99%':<10} | {'ES 99%':<10}"
        )
        print("-" * 80)
        for r in runs:
            print(
                f"{r.id:<4} | {r.run_timestamp!s:<20} | {r.portfolio_id:<15} | {r.var_99:<10.4f} | {r.expected_shortfall_99:<10.4f}"
            )
            print(
                f"     -> Kupiec p-val: {r.kupiec_p_value:.4f} | Christoffersen p-val: {r.christoffersen_p_value:.4f} | Status: {r.status}"
            )
        print("=" * 80 + "\n")
    finally:
        session.close()


if __name__ == "__main__":
    main()
