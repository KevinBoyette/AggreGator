SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
.RECIPEPREFIX = >

default: build
.PHONY: all build clean deps format help lint list purge test

help:
> @echo "Usage:"
> @echo -e "\tmake <target(s)>\n"
> @echo "Targets:"
> @tabs 24
> @sed -n '/^# @help:/{N;p;}' Makefile | sed 's/^#.*: //g' | sed 's/:.*$$//g' | tac | paste -s -d"\t\n" | sed 's/^/    /g' | tac
> @tabs 4

# @help: Install dependencies
deps:
> @poetry install

# TODO: build is maybe misleading. I actually just want to verify types here
# @help: Default target (just run `make`). Does nothing ATM
build:
> @echo pytype?

# @help: Run all tests
test:
> @poetry run pytest --cov --cov-report term:skip-covered

# @help: Lint and format all files
format:
> @poetry run isort --quiet .
> @poetry run autopep8 src/

# @help: Lint all files and report violations
lint:
> @poetry run pylint src/

# @help: Delete build output and crud that that piles up in the workspace
clean:
> @find src -name '__pycache__' | xargs rm -rf
> @rm -rf .coverage .pytest_cache/

# @help: Run clean first and then delete dependencies and lockfile(s)
purge: clean
> @rm -rf poetry.lock .venv/*

# @help: List __init__.py files and disabled lint rules
list:
> @echo "All __init__.py:"
> @find src -name '__init__.py'
> @echo "Disabled lint rules:"
> @find src -name '*.py' | xargs grep -nH "pylint: disable"

# @help: format build and test
all: format build test
