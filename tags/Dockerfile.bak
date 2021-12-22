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
        libxml2-dev \
        libxslt1-dev \
        libsasl2-dev \
        zlib1g-dev \
        g++ \
        libldap2-dev \
        libssl-dev \
        graphviz \
        libgraphviz-dev \
        libpq-dev \
        make \
 && rm -rf /var/lib/apt/lists/*

# copy code
COPY clusterisation/ clusterisation/
# copy libs
COPY db_lib/ db_lib/
# copy env
COPY .env .env


WORKDIR /code/clusterisation/

# install dependencies
RUN make venv
## drop poetry
RUN pip uninstall --yes poetry
## run it
ENTRYPOINT ["make", "cluster-last"]