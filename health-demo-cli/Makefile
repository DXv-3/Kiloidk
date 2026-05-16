.PHONY: install start start-backend start-frontend docker-up docker-down seed reset test lint format type-check build clean health

install:
	bun install --cwd frontend
	pip install -e .

start: start-backend start-frontend

start-backend:
	uvicorn backend.main:app --reload --port 8000

start-frontend:
	cd frontend && bun dev

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

seed:
	echo "Seeding data..."

reset:
	echo "Resetting..."

test:
	echo "Testing..."

lint:
	ruff check backend
	cd frontend && eslint .

format:
	ruff format backend
	cd frontend && prettier --write .

type-check:
	mypy backend
	cd frontend && tsc --noEmit

build:
	cd frontend && bun build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf node_modules .next

health:
	curl http://localhost:8000/health
