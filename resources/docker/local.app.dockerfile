FROM python:3.12-slim

# ---- recommended environment variables ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN pip install --no-cache-dir uv \
    && uv venv \
    && uv sync --group app --group local

EXPOSE 8000

ENTRYPOINT ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
