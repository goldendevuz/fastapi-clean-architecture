FROM python:3.12-slim

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN pip install --no-cache-dir uv \
    && uv venv \
    && uv sync --group linters

CMD ["tail", "-f", "/dev/null"]
