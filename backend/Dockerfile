FROM python:3.10-slim as base

WORKDIR /app

# Setup env
ENV LANG C.UTF-8 \
  LC_ALL C.UTF-8 \
  PYTHONDONTWRITEBYTECODE 1 \
  PYTHONFAULTHANDLER 1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_VERSION=1.6.1

# Install dependencies
FROM base AS deps

# Install poetry
RUN pip install poetry==1.6.1

# Install python dependencies in /app/.venv
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --without dev && rm -rf $POETRY_CACHE_DIR


FROM base AS runtime

# Copy virtual env from deps stage
ENV VIRTUAL_ENV=/app/.venv
COPY --from=deps $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="/app/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd -m appuser
USER appuser

# Install application into container
COPY . .

EXPOSE 5000

# Run the application
CMD ["python", "main.py"]