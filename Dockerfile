FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY server /app/server

WORKDIR /app/server/frontend
RUN npm ci || npm install
RUN npm run build

WORKDIR /app/server/backend

ENV PORT=8000
EXPOSE 8000

CMD sh -c "python manage.py migrate --noinput || true && python manage.py collectstatic --noinput || true && gunicorn dealership.wsgi:application --bind 0.0.0.0:"
