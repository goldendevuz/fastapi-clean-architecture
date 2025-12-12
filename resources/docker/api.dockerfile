FROM python:3.13.11-slim

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN pip install uv --no-cache-dir

COPY . .

ENTRYPOINT ["sh", "sleep infinity"]