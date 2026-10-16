.PHONY: install migrate test run clean

install:
	poetry install

migrate:
	poetry run alembic upgrade head

test:
	poetry run pytest tests/ -v

run:
	poetry run python -m risk_runner.runner

clean:
	rm -f risk_local.db
	find . -type d -name "__pycache__" -exec rm -r {} +