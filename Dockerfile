# syntax=docker/dockerfile:1
FROM oven/bun:1 AS frontend-build
WORKDIR /build
COPY frontend ./frontend
WORKDIR /build/frontend
RUN bun install
RUN bun run build

FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY src ./src
COPY --from=frontend-build /build/frontend/dist ./dist
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
