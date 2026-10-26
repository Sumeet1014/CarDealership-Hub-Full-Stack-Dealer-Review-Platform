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

# Render injects the PORT environment variable at runtime; bind to it directly.
# migrate, seed and collectstatic are NOT followed by `|| true` so a failure
# fails the deploy instead of silently starting with an uninitialized database.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_data && python manage.py collectstatic --noinput && gunicorn dealership.wsgi:application --bind 0.0.0.0:$PORT"]
