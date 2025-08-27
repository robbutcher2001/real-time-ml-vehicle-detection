FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg

COPY pyproject.toml poetry.lock .

RUN pip install poetry && \
    poetry install --only main --no-root

COPY . .

RUN poetry install --only main

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "rtvd.server:app"]
