DB_LIB = ../db_lib

VENV ?= .venv

all: up

venv_rm:
	rm -rf $(VENV)

venv:
	python3.8 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install --no-compile poetry
	$(VENV)/bin/python -m pip install natasha
	$(VENV)/bin/poetry config virtualenvs.create false
	$(VENV)/bin/poetry install --no-dev --no-interaction --no-ansi

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

tag-old:
	$(VENV)/bin/python tag.py --start_date=2012-09-05 --end_date=2021-12-05

tag:
	$(VENV)/bin/python tag.py --start_date=2021-12-11 --end_date=2021-12-15

tag-last:
	$(VENV)/bin/python tag.py --start_date=2021-12-16

tag-local:
	$(VENV)/bin/python tag.py

up:
	/etc/init.d/cron start
	crontab $(CODE)/cron_schedule.txt
	touch all.log
	tail -f all.log

service:
	docker-compose build
	docker-compose up

ci:	lint test