CODE = web_service/web_service/src
TESTS = web_service/tests

ALL = $(CODE) $(TESTS)

VENV ?= .venv

clean_all_local: venv_rm cleanup poetry_lock venv

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
	$(VENV)/bin/alembic -c db_lib/alembic.ini revision --autogenerate -m 'Added required tables'
	$(VENV)/bin/alembic -c db_lib/alembic.ini upgrade head

populate:
	$(VENV)/bin/python $(CODE)/scripts/populate.py

up:
	$(VENV)/bin/python $(CODE)/run_server.py

service:
	docker compose build
	docker compose up

ci:	lint test

cleanup:
	docker container prune
	docker image prune
	docker volume prune
	docker system prune
	docker builder prune
	rm -rf migrations
	rm -rf postgres*
	rm -rf db_lib/dist

poetry_lock:
	cd parser && poetry lock
	cd web_service && poetry lock
	cd ml_jobs && poetry lock

cluster:
	$(VENV)/bin/python $(CODE)/clusterisation.py