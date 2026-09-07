# Automated Serverless Quantitative Risk Pipeline (`cloud-risk-pipeline`)

An infrastructure-as-code (IaC) driven serverless batch processing platform on AWS. Automates end-to-end daily portfolio risk computations (VaR, Expected Shortfall, GARCH volatility updates) using scheduled event triggers, ephemeral containerized tasks, relational metadata tracking, and zero-idle cloud infrastructure.

---

## 1. Architectural & Engineering Directives

- **Infrastructure as Code (IaC):** 100% defined via modular **Terraform** (AWS VPC, public/private subnets, IAM least-privilege roles, S3 data buckets, ECS Cluster, and ECR).
- **Containerized Serverless Execution:** Calculation engine packaged in a minimal, multi-stage `python:3.12-slim` Docker image deployed to **AWS ECS on Fargate**. Zero EC2 instance management, zero idle compute spend.
- **Event Orchestration:** AWS EventBridge (cron trigger) invoking AWS Step Functions or direct ECS RunTask to schedule end-of-day risk runs upon market close.
- **State & Auditability:** PostgreSQL (AWS RDS / local containerized Postgres) tracking daily model runs, execution runtimes, parameter versions, and VaR breach logs using **Alembic** migrations.
- **Data Persistence:** Raw portfolio input weights and generated risk attribution matrices stored in encrypted S3 buckets with lifecycle retention rules.

---

## 2. Directory Layout

```text
cloud-risk-pipeline/
├── terraform/
│   ├── main.tf              # Provider configuration and module calls
│   ├── variables.tf         # Environment, VPC, and container task parameters
│   ├── outputs.tf           # RDS endpoint, ECR repo URL, S3 bucket names
│   └── modules/
│       ├── networking/      # VPC, subnets, route tables, security groups
│       ├── storage/         # S3 buckets and RDS PostgreSQL instance
│       └── compute/         # ECS Cluster, Task Definition, and IAM roles
├── docker/
│   └── Dockerfile           # Minimal Python 3.12-slim runtime container
├── src/
│   └── risk_runner/
│       ├── __init__.py
│       ├── config.py        # Environment variable ingestion via Pydantic Settings
│       ├── db.py            # SQLAlchemy 2.0 / Alembic models for risk audit runs
│       └── runner.py        # Batch task pulling S3 portfolios, computing VaR/ES
└── tests/
    └── test_pipeline_runner.py
```
