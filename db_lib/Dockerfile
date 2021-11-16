FROM python:3.8-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONFAULTHANDLER=true
ENV PYTHONUNBUFFERED=true

WORKDIR /code/

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        gcc \
        libsasl2-dev \
        libldap2-dev \
        libssl-dev \
        graphviz \
        libgraphviz-dev \
        libpq-dev \
        make \
 && rm -rf /var/lib/apt/lists/*

# copy poetry
COPY pyproject.toml /code/
COPY poetry.lock /code/
# copy project
COPY db_lib /code/db_lib

# install dependencies
RUN python -m venv .venv \
 && pip install --no-compile --upgrade pip \
 && pip install --no-compile poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi \
 && pip uninstall --yes poetry

# copy src
COPY web_service/src/ /code/web_service/src/
COPY data /code/data
COPY Makefile /code/

# run it
ENTRYPOINT [""]
CMD ["make"]