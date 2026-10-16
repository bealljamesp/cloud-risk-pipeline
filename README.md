# Local Quantitative Risk Pipeline

A local, automated quantitative risk engine built in Python 3.12 for calculating Value-at-Risk and Expected Shortfall using GJR-GARCH conditional volatility simulation paths and regulatory backtesting. Designed for portfolio risk analysis and institutional audit readiness.

## Core Features

* **GJR-GARCH Volatility Modeling:** Computes dynamic conditional variance paths incorporating asymmetric leverage effects for negative market shocks.
* **Vectorized Monte Carlo Engine:** Generates large-scale multi-period asset paths leveraging high-performance NumPy linear algebra operations without explicit Python loops.
* **Regulatory Backtesting Suite:** Implements the Kupiec Proportion of Failures test and the Christoffersen Markov chain independence test to evaluate exception frequencies and clustering.
* **Persistent Audit Ledger:** Automatically records run timestamps, risk metrics, and backtest p-values to a local SQLite database using SQLAlchemy.
* **Automation:** Manages environment setup, testing, and execution tasks via Poetry and GNU Make.

## Project Structure

```text
cloud-risk-pipeline/
├── data/
│   └── portfolio_weights.csv
├── src/
│   └── risk_runner/
│       ├── __init__.py
│       ├── backtest.py
│       ├── config.py
│       ├── db.py
│       ├── garch.py
│       ├── main.py
│       ├── models.py
│       └── runner.py
├── tests/
│   ├── test_backtest.py
│   ├── test_garch.py
│   ├── test_pipeline_runner.py
│   └── test_simulation.py
├── main.py
├── Makefile
├── pyproject.toml
└── README.md
```

---

## Quick Start

```
make install

make test

make run
```

## Sample Execution Output

```
2026-10-16 14:57:13,562 [INFO] __main__: Starting local quantitative risk pipeline execution.
2026-10-16 14:57:13,563 [INFO] risk_runner.runner: Initializing risk calculation runner.
2026-10-16 14:57:13,563 [INFO] risk_runner.runner: Loading local portfolio weights from data/portfolio_weights.csv
2026-10-16 14:57:13,567 [INFO] risk_runner.runner: Calculated VaR (99.0%): 0.058000 | ES: 0.067287 | Kupiec p-val: 0.0244 | Christoffersen p-val: 1.0000
2026-10-16 14:57:13,579 [INFO] risk_runner.runner: Successfully persisted GARCH metrics and backtest results to metadata ledger.

================================================================================
ID   | TIMESTAMP (UTC)      | PORTFOLIO       | VaR 99%    | ES 99%    
--------------------------------------------------------------------------------
4    | 2026-10-16 21:57:13.569455 | portfolio_main  | 0.0580     | 0.0673    
     -> Kupiec p-val: 0.0244 | Christoffersen p-val: 1.0000 | Status: SUCCESS
3    | 2026-10-16 21:54:22.730724 | portfolio_main  | 0.0580     | 0.0673    
     -> Kupiec p-val: 0.0244 | Christoffersen p-val: 1.0000 | Status: SUCCESS
2    | 2026-10-16 21:53:57.632259 | portfolio_main  | 0.0580     | 0.0673    
     -> Kupiec p-val: 0.0244 | Christoffersen p-val: 1.0000 | Status: SUCCESS
1    | 2026-10-16 21:53:24.461164 | portfolio_main  | 0.0580     | 0.0673    
     -> Kupiec p-val: 0.0244 | Christoffersen p-val: 1.0000 | Status: SUCCESS
================================================================================
```