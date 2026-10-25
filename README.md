# Cars Dealership

Full-stack car dealership review application built for the Coursera Full-Stack Capstone.

## Technology Stack

- **Backend:** Python, Django, Django REST Framework, SQLite, Django authentication
- **Frontend:** React (Vite), JavaScript, React Router, HTML/CSS
- **Additional:** REST APIs, sentiment analysis, Docker, Kubernetes, GitHub Actions, IBM Cloud Code Engine preparation

## Project Structure

```
Cars Dealership/
├── server/
│   ├── backend/            # Django project (dealership/)
│   │   ├── manage.py
│   │   └── dealership/     # settings, urls, wsgi/asgi
│   └── frontend/           # React application (Vite)
│       ├── src/
│       └── package.json
├── evidence/               # Real cURL evidence captured from running app
├── k8s/                    # Kubernetes manifests
├── .github/workflows/      # CI/CD
├── requirements.txt
├── .env.example
└── README.md
```

## Local Setup

### Prerequisites

- Python 3.12+
- Node.js 18+

### Backend

```bash
python -m pip install -r requirements.txt
cd server/backend
python manage.py migrate
python manage.py runserver
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd server/frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## Status

Phase 1 (project setup) complete. API, authentication, reviews, sentiment analysis, Docker, Kubernetes, CI/CD and deployment preparation follow in later phases.
