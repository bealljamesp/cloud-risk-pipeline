from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    aws_region: str = "us-west-2"
    s3_bucket_name: str
    database_url: str
    portfolio_file_key: str = "inputs/portfolio_weights.csv"
    confidence_level: float = 0.99
    simulation_runs: int = 10000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
