FROM python:3.10.2-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    # poetry
    POETRY_VERSION=1.2.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false

ENV PATH="$POETRY_HOME/bin:$PATH"

FROM base AS app

RUN apt-get update  \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    libpq-dev \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL https://install.python-poetry.org | python - \
    && poetry --version \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y  \
    && rm -rf /var/lib/apt/lists/*


COPY ./poetry.lock ./pyproject.toml /app/

WORKDIR /app
RUN poetry config virtualenvs.create false && poetry install --no-ansi

COPY ./src/* /app/
WORKDIR /app