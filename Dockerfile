FROM python:3.10.12-slim-buster

WORKDIR /app
COPY . /app

RUN apt update && \
    apt upgrade -y && \
    apt install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c "pip install --no-cache-dir -r requirements.txt"

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:app"]