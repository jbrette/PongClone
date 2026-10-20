FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    alsa-utils \
    libtk8.6 \
    mpg123 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON_PREFERENCE=only-system

COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --locked

COPY src/ ./src/

# Sound files are referenced by relative path, so run from src/.
WORKDIR /app/src
CMD [ "uv", "run", "--locked", "--no-sync", "Pong_Clone.py" ]
