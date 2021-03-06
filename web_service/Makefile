CODE = web_service/src
TESTS = web_service/tests
DB_LIB = ../db_lib

ALL = $(CODE) $(TESTS)

VENV ?= .venv

all: migrate up

venv_rm:
	rm -rf $(VENV)

venv:
	python3.8 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install --no-compile poetry
	$(VENV)/bin/poetry config virtualenvs.create false
	$(VENV)/bin/poetry install --no-dev --no-interaction --no-ansi

test:
	$(VENV)/bin/pytest -v tests

lint:
	$(VENV)/bin/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV)/bin/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/bin/black --skip-string-normalization --check $(ALL)
	$(VENV)/bin/mypy $(CODE)

format:
	$(VENV)/bin/isort --apply --recursive $(ALL)
	$(VENV)/bin/black --skip-string-normalization $(ALL)
	$(VENV)/bin/autoflake --recursive --in-place --remove-all-unused-imports $(ALL)
	$(VENV)/bin/unify --in-place --recursive $(ALL)

migrate:
	$(VENV)/bin/alembic -c $(DB_LIB)/alembic.ini revision --autogenerate -m 'Added required tables'
	$(VENV)/bin/alembic -c $(DB_LIB)/alembic.ini upgrade head

up:
	$(VENV)/bin/python $(CODE)/run_server.py

ci:	lint test