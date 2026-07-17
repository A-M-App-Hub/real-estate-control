# syntax=docker/dockerfile:1
FROM python:3.13-slim
WORKDIR /app

# Instalar uv
RUN pip install --no-cache-dir uv

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock* ./

# Instalar dependências
RUN uv sync --frozen || uv sync

# Copiar código
COPY . .

# Frontend já está em frontend/dist/ (commitado)
# StaticFiles serve de ./dist/ então copiamos para lá
RUN if [ -d frontend/dist ] && [ "$(ls -A frontend/dist)" ]; then \
      cp -r frontend/dist/. ./dist/; \
    else \
      echo "WARNING: frontend/dist/ is empty or missing"; \
      mkdir -p ./dist; \
    fi

EXPOSE 8080
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
