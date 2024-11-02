.PHONY: all run redis tests lint
.SILENT: all run redis tests lint

export APP_HOST
export APP_PORT
export POSTGRES_HOST
export POSTGRES_PORT
export REDIS_PASSWORD

WORKDIR=src
FLAGS=--config pyproject.toml

all: run tests lint

run:
	echo "Starting server..."
	poetry run uvicorn $(WORKDIR).main:app --host $(APP_HOST) --port $(APP_PORT)

redis:
	mkdir -p /usr/local/etc/redis
    echo "bind 0.0.0.0" > /usr/local/etc/redis/redis.conf
    echo "requirepass $(REDIS_PASSWORD) >> /usr/local/etc/redis/redis.conf
    redis-server /usr/local/etc/redis/redis.conf

# tests:
# 	@echo "Running tests..."
# 	@poetry run pytest $(WORKDIR)/tests

lint:
	echo "Linting..."
	poetry run black ./$(WORKDIR) $(FLAGS)
	echo "Linting done."

