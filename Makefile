# # # Setting up Makefile behavior
.SILENT:

# Compose file combinations
COMPOSE_LOCAL      := docker compose -f docker-compose.yaml -f ./resources/docker/local.docker-compose.yaml

# Docker Commands
up:
	$(COMPOSE_LOCAL) up -d

down:
	$(COMPOSE_LOCAL) down

logs:
	$(COMPOSE_LOCAL) logs -f

build:
	$(COMPOSE_LOCAL) build

rebuild:
	$(MAKE) down
	$(MAKE) build
	$(MAKE) up

restart:
	$(COMPOSE_LOCAL) restart app


# Linter Commands
lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

lint-fix-unsafe:
	uv run ruff check . --fix --unsafe-fixes

lint-type:
	uv run pyright

# Dependency Commands
sync:
	uv sync --all-groups

lock:
	uv lock

# Migration Commands
migrate-head:
	$(COMPOSE_LOCAL) exec api uv run alembic upgrade head

migrate-base:
	$(COMPOSE_LOCAL) exec api uv run alembic downgrade base

migrate-new:
	$(COMPOSE_LOCAL) exec api uv run alembic stamp head

migrate-collect:
	$(COMPOSE_LOCAL) exec api uv run alembic revision --autogenerate

migrate-up:
	$(COMPOSE_LOCAL) exec api uv run alembic upgrade +1

migrate-down:
	$(COMPOSE_LOCAL) exec api uv run alembic downgrade -1

# Shell Open Commands
shell:
	$(COMPOSE_LOCAL) exec api bash

shell-db:
	$(COMPOSE_LOCAL) exec database psql -U postgres -d postgres

# Tree Command
tree:
	tree > tree.txt
