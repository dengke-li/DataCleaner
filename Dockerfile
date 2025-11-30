# ==========================================
# Stage 1: Builder (Installs tools & deps)
# ==========================================
FROM python:3.10-slim as builder

# Set env variables to configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install Poetry (using pip is often easiest in Docker)
RUN pip install poetry

WORKDIR /app

# Copy only the dependency files first (to cache the dependency layer)
COPY pyproject.toml poetry.lock README.md ./

# Install dependencies (no-root skips installing the app itself for now)
# --no-root is important because we haven't copied source code yet
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# ==========================================
# Stage 2: Runtime (Production Image)
# ==========================================
FROM python:3.10-slim as runtime

# Set env variables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy your actual application code
COPY app ./app
COPY *.py ./

EXPOSE 8000
# Run the application
#CMD ["python", "api.py"]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]