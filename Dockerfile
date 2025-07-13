FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt update && apt install -y \
    build-essential \
    libpq-dev \
    curl \
    redis \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt