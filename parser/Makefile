CODE =
TESTS = test

ALL = $(CODE) $(TESTS)

VENV ?= .venv

all:up

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

up:
	$(VENV)/bin/python parse_news.py -d vk.json vk_db -start_urls url_files/vk.url
	$(VENV)/bin/python parse_news.py -d rss_news.json rss_db -s url_files/smi.url -r data_collection/rss_parser.yaml

ci:	lint test
