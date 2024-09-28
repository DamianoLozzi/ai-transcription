FROM python:3.10.12-slim-buster

WORKDIR /app
COPY . /app

RUN apt update && \
    apt upgrade -y && \
    apt install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c "pip install --upgrade pip;pip install --no-cache-dir -r requirements.txt"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000/ || exit 1

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:app"]