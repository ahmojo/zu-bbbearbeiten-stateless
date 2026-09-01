FROM python:3.11-slim@sha256:d1e9ca7c4e78d1e8ecadb5d44bfc8e956e7a65b659a9950f569f243d72b326d0

LABEL org.opencontainers.image.source="https://github.com/ahmojo/zu-bbbearbeiten-stateless"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY helper.py main.py ./
COPY templates ./templates

USER app
EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "main:app"]
