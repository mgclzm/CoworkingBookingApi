FROM python:3.14-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked 

COPY . .

EXPOSE 8000

# CMD ["uv", "run", "uvicorn", "api/app:init_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]