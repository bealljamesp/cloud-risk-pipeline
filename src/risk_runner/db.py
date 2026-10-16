from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from risk_runner.config import settings

Base = declarative_base()


class RiskRunModel(Base):
    __tablename__ = "risk_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_timestamp = Column(DateTime, default=datetime.utcnow)
    portfolio_id = Column(String, default="portfolio_main")
    var_99 = Column(Float, nullable=False)
    expected_shortfall_99 = Column(Float, nullable=False)
    kupiec_p_value = Column(Float, nullable=True)
    christoffersen_p_value = Column(Float, nullable=True)
    status = Column(String, nullable=False)


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
