.PHONY: all run tests lint

export app_host
export app_port

WORKDIR=src
FLAGS=--config pyproject.toml

all: run tests lint

run:
	@echo "Starting server..."
	@poetry run uvicorn $(WORKDIR).main:app --reload --host $(app_host) --port ${app_port}

# tests:
# 	@echo "Running tests..."
# 	@poetry run pytest $(WORDDIR)/tests

lint:
	@echo "Linting..."
	@poetry run black ./$(WORKDIR) $(FLAGS)
	@echo "Linting done"