.PHONY: all run tests lint

export $(shell sed 's/=.*//' .env)

WORDDIR=./src
FLAGS=--config pyproject.toml

all: run tests lint

run:
	@echo "Starting server..."
	@poetry run python3 $(WORDDIR)/main.py

# tests:
# 	@echo "Running tests..."
# 	@poetry run pytest $(WORDDIR)/tests

lint:
	@echo "Linting..."
	@poetry run black $(WORDDIR) $(FLAGS)
	@echo "Linting done"