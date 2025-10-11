FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# deps + extras for EmailStr
RUN python -m pip install -U pip && \
    pip install -e . && \
    pip install "pydantic[email]>=2.8.2" pytest-xdist allure-pytest

CMD ["bash", "-lc", "pytest -m 'live or contract' -n auto --alluredir=allure-results"]