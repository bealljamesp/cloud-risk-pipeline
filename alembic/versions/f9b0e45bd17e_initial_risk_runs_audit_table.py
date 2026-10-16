"""Initial risk runs audit table

revision = "f9b0e45bd17e"
Revises:
Create Date: 2026-10-16 13:43:00.000000

"""

import sqlalchemy as sa

from alembic import op

revision = "<revision_id>"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "risk_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_timestamp", sa.DateTime(), nullable=False),
        sa.Column("portfolio_id", sa.String(length=64), nullable=False),
        sa.Column("var_99", sa.Float(), nullable=False),
        sa.Column("expected_shortfall_99", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_risk_runs_portfolio_id"), "risk_runs", ["portfolio_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_risk_runs_portfolio_id"), table_name="risk_runs")
    op.drop_table("risk_runs")
