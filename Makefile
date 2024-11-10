.PHONY: all run tests lint
.SILENT: all run tests lint

export $(cat .env | grep -v ^# | xargs)
export $(cat .env.test | grep -v ^# | xargs)

WORKDIR=src
FLAGS=--config pyproject.toml 

all: # no op

run:
	docker-compose -f docker-compose.yml up -d --build

tests:
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit --build || true
	docker-compose -f docker-compose.test.yml down --volumes


lint:
	poetry run black ./$(WORKDIR) $(FLAGS)
	poetry run mypy ./$(WORKDIR) $(FLAGS)

