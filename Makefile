.PHONY: migrations
.PHONY: tests

# Command to display available commands
help:
	@echo "Available commands:"
	@echo "  make build                 - Build the development server Docker images"
	@echo "  make build-no-cache        - Build the server without using Docker cache"
	@echo "  make run                   - Start the API development server"
	@echo "  make migrate               - Apply database migrations"
	@echo "  make install_pre_commit    - Install pre-commit and set up hooks for this repository"
	@echo "  make run_pre_commit        - Run pre-commit hooks on all files manually"


build:
	@echo "Building development server docker"
	docker compose build

build-no-cache:
	@echo "Building development server docker without cache"
	docker compose build --no-cache

run:
	@echo "starting API development server docker"
	docker compose up

migrations:
	@echo "making migrations"
	docker compose run --rm web alembic revision --autogenerate -m "$(name)"

migrate:
	@echo "migrating"
	docker compose run --rm web alembic upgrade head

install_pre_commit:
	@echo "Ensuring pre-commit is installed and hooks are set up..."
	pip install pre-commit && pre-commit install && pre-commit autoupdate

run_pre_commit:
	@echo "Running pre-commit hooks on all files..."
	pre-commit run --all-files