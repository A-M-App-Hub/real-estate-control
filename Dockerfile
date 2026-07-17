FROM python:3.13-slim
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv && uv --version

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen && uv pip list

# Copy application code
COPY src ./src
COPY frontend/dist ./dist

# Verify files
RUN ls -la && ls -la src/ && ls -la dist/

EXPOSE 8080
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
