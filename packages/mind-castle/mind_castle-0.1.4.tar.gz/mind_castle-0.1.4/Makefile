install:
	pip install uv
	uv sync

install_dev:
	pip install uv
	uv sync --dev

precommit:
	pre-commit install
	pre-commit run --files $$(git diff --cached --name-only)

test:
	pytest -v

lint:
	black .
	flake8 .

build:
	uv build

# NOTE: You need to set UV_PUBLISH_TOKEN in your terminal
publish:
	uv publish

.PHONY: install install_dev precommit test lint build
