# Deployment Guide

## Render Deployment

The container runs these commands on every start (see `Dockerfile`):

1. `python manage.py migrate --noinput`
2. `python manage.py seed_data`
3. `python manage.py collectstatic --noinput`
4. `gunicorn dealership.wsgi:application --bind 0.0.0.0:$PORT`

`seed_data` is idempotent, so it is safe to run on every restart. It initializes
the existing dealers, car makes/models, reviews and the demo login user. If any
step fails, the deploy fails instead of starting with an empty database.

### Required Render environment variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key (keep private) |
| `DEBUG` | Set to `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hosts, e.g. `cars-dealership-qfx2.onrender.com` |
| `SEED_DEMO_USERNAME` | Username for the seeded login/review account |
| `SEED_DEMO_EMAIL` | Email for the seeded account |
| `SEED_DEMO_PASSWORD` | Password for the seeded account (keep private) |

On a fresh database, `seed_data` requires `SEED_DEMO_USERNAME` and
`SEED_DEMO_PASSWORD`; it fails with a clear error if they are missing. The
password is hashed with Django's password hasher and is never written to logs.

### IBM Cloud Code Engine Deployment

This application is also prepared for deployment to IBM Cloud Code Engine. Do NOT guess credentials/URLs - perform deployment with your own IBM Cloud account.

### Prerequisites
- IBM Cloud account
- IBM Cloud CLI installed
- Docker installed

### Steps
1. Login to IBM Cloud: ibmcloud login
2. Target resource group and region
3. Create/select Code Engine project
4. Build and push Docker image
5. Create app with port 8000
6. Get app URL

### Notes
- Update environment variables as needed
- SQLite is used for local dev
