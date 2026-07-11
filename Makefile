.PHONY: install dev worker test test-e2e test:e2e lint format typecheck migrate seed clean

install:
	cd frontend && npm install
	python -m pip install -e ".[dev]"

dev:
	cd frontend && npm run dev

worker:
	python -m backend.workers.local_worker

test:
	pytest
	cd frontend && npm test

test-e2e:
	cd frontend && npm run test:e2e

test\:e2e: test-e2e

lint:
	ruff check backend
	cd frontend && npm run lint

format:
	ruff format backend
	cd frontend && npm run format

typecheck:
	mypy backend/app
	cd frontend && npm run typecheck

migrate:
	python -m backend.app.db.migrate

seed:
	python -m backend.app.db.seed

clean:
	python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.mypy_cache', '.ruff_cache', 'frontend/dist', 'frontend/node_modules']]"
