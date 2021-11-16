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

COPY Makefile /code/

# copy libs
COPY db_lib /code/db_lib

# copy poetry
COPY pyproject.toml /code/
COPY poetry.lock /code/

# install dependencies
RUN make venv

# drop poetry
RUN pip uninstall --yes poetry

# copy src
COPY web_service/src/ /code/web_service/src/
COPY parser /code/parser/
COPY .env /code/.env

# run it
ENTRYPOINT [""]
CMD ["make"]