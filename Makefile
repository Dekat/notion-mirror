SHELL = /bin/bash

APP_NAME=notion_mirror

DOCKER_COMPOSE_RUN = docker-compose -f docker-compose.yml run --rm
DOCKER_COMPOSE_RUN_DEV = docker-compose -f docker-compose-dev.yml run --rm

## help: Display list of commands (from gazr.io)
.PHONY: help
help: Makefile
	@sed -n 's|^##||p' $< | column -t -s ':' | sed -e 's|^| |'

## style: Check lint, code styling rules. e.g. pylint, phpcs, eslint, style (java) etc ...
.PHONY: style
style:
	${DOCKER_COMPOSE_RUN_DEV} -T --no-deps \
		app bash -c " \
			pipenv run flake8 $(APP_NAME) tests *.py; \
			pipenv run mypy $(APP_NAME) *.py; \
			pipenv run black --check $(APP_NAME) tests *.py"

 ## Cyclomatic complexity (McCabe) and maintainability check
.PHONY: complexity
complexity:
	${DOCKER_COMPOSE_RUN_DEV} -T --no-deps \
		app bash -c \
		"pipenv run radon cc -s -n B $(APP_NAME) | tee /tmp/cc.txt && if [ -s /tmp/cc.txt ]; then exit 1; fi; \
		pipenv run radon mi -n B $(APP_NAME) | tee /tmp/mi.txt && if [ -s /tmp/mi.txt ]; then exit 1; fi"

## format: Format code. e.g Prettier (js), format (golang)
.PHONY: format
format:
	${DOCKER_COMPOSE_RUN_DEV} -T --no-deps \
	    	app bash -c \
	    	"pipenv run isort $(APP_NAME) tests *.py;\
	    	pipenv run black $(APP_NAME) tests *.py"

## test: Shortcut to launch all the test tasks (unit, functional and integration).
.PHONY: test
test:
	${DOCKER_COMPOSE_RUN_DEV} \
		app bash -c "PYTHONPATH=. pipenv run pytest -vvv --cov . --cov-config .coveragerc --cov-report term-missing tests"

## Build or rebuild the services
.PHONY: build
build:
	-docker-compose -f docker-compose.yml build \
	--force-rm --no-cache \
	--build-arg USER_UID=$(shell id -u $$USER) \
	--build-arg USER_GID=$(shell id -g $$USER)

## Build or rebuild the services for the dev environment
.PHONY: build-dev
build-dev:
	-docker-compose -f docker-compose-dev.yml build \
	--force-rm --no-cache \
	--build-arg USER_UID=$(shell id -u $$USER) \
	--build-arg USER_GID=$(shell id -g $$USER)

## run: Locally run the application, e.g. node index.js, python -m myapp, go run myapp etc ...
.PHONY: run
run:
	-${DOCKER_COMPOSE_RUN} app # the dash ignore error code when CTRL-C is pressed

.PHONY: shell
shell:
	-${DOCKER_COMPOSE_RUN} app bash # the dash ignore error code when CTRL-C is pressed

## clean: Remove temporary files and docker images
.PHONY: clean
clean:
	find . -type f -name "*.log" -exec rm {} + || true
	docker-compose -f docker-compose.yml down -v --remove-orphans
	docker-compose -f docker-compose.yml rm -v
	rm -rf ./cache/*
