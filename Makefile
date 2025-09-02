SHELL := /bin/bash

.PHONY: run lint test build

run:
	poetry run python -m app.main

lint:
	flake8 app tests

test:
	pytest --maxfail=1 --disable-warnings

build:
	docker compose up --build
