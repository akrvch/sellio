FROM python:3.13.2-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ Europe/Kiev

ENV UV_SYSTEM_PYTHON=1

COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-dev --frozen --no-install-project

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

# ==== image for local dev (no need to copy, because dev image is mounted)
FROM base as dev

ENV SELLIO__ENV dev
ENTRYPOINT ["uv", "run"]

# ==== image for possible deploy
FROM base as prd
COPY sellio /app/sellio
COPY config /app/config

ENV SELLIO__ENV prd
ENTRYPOINT ["uv", "run"]
CMD ["uvicorn" ,"sellio.main:app", "--host", "0.0.0.0", "--port", "8080"]
