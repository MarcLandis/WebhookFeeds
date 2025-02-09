FROM unit:1.34.1-python3.13-slim

LABEL authors="MarcLandis"

# `WEBHOOKFEEDS_ENV` arg is used to make prod / dev builds:
ARG WEBHOOKFEEDS_ENV

ENV WEBHOOKFEEDS_ENV=${WEBHOOKFEEDS_ENV} \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry:
    POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    # fastapi:
    URL_SUBFOLDER='/api'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL 'https://install.python-poetry.org' | python -

WORKDIR /usr/src

COPY ./poetry.lock ./pyproject.toml /usr/src/

COPY ./LICENSE.md /usr/src/LICENSE.md
COPY ./README.md /usr/src/README.md
COPY ./.assets /usr/src/.assets

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
    poetry sync \
    $(if [ "$WEBHOOKFEEDS_ENV" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi

COPY ./app /usr/src/app
COPY ./config.json /docker-entrypoint.d/config.json

RUN chown -R unit:unit /usr/src/

EXPOSE 80
