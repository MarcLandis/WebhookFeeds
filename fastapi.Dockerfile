FROM python:3.13-alpine

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
  POETRY_HOME='/usr/local'

RUN apk add --no-cache curl libpq

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

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
