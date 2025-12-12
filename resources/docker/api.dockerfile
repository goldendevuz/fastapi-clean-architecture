FROM python:3.13.11-slim

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN pip install uv --no-cache-dir

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "sleep infinity"]