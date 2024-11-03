.PHONY: all run tests lint
.SILENT: all run tests lint

export APP_HOST
export APP_PORT

export POSTGRES_HOST
export POSTGRES_PORT

WORKDIR=src
FLAGS=--config pyproject.toml

all: run redis tests lint 

run:
	echo "Starting server..."
	poetry run uvicorn $(WORKDIR).main:app --host $(APP_HOST) --port $(APP_PORT)

# tests:
# 	@echo "Running tests..."
# 	@poetry run pytest $(WORKDIR)/tests

lint:
	echo "Linting..."
	poetry run black ./$(WORKDIR) $(FLAGS)
	echo "Linting done."

