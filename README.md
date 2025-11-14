# Travel Planner Backend (Django + DRF)

Backend API that powers the Travel Planner experience. Provide a budget, preferred region, and lifestyle, and the service returns curated itineraries generated from real travel data. Users can confirm a plan, store it for later, and filter historical trips.

---

## 🔧 Tech Stack

- Python 3.12
- Django 5.x + Django REST Framework
- SQLite (development database)
- pandas/numpy for travel-plan generation
- Gunicorn for production serving

---

## 🚀 Features

- Generate three itineraries customized by budget, region, and lifestyle
- Persist confirmed trips and expose them via REST
- Filter stored trips by region/lifestyle query params
- Currency conversion + lifestyle-aware activity selection

---

## 📁 Project Structure

```
travel-planner-backend/
│
├── ml_models/                  # Data-driven planning logic + datasets
├── trips/                      # Django app (models, views, serializers, URLs)
├── config/                     # Django project configuration
├── scripts/                    # Tooling helpers (e.g., version bumper)
├── Makefile / pyproject.toml   # Build + packaging definitions
├── VERSION                     # Authoritative semantic version
├── requirements.txt            # Runtime dependencies (pinned)
├── runtime.txt / Procfile      # Deployment hints (Render/Heroku-style)
└── manage.py                   # Django entrypoint
```

---

## ✅ Prerequisites

- Python **3.12** (recommended to install via `pyenv` or your OS package manager)
- `pip` 24+ (installed automatically via `make deps`)
- Optional but recommended: virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`)
- SQLite (bundled with Python; no manual install required)

---

## 🧭 Local Setup

1. **Clone** the repo and `cd` into it.
2. *(Optional)* Create/activate a virtual environment.
3. **Install dependencies & tooling**: `make deps`
4. **Apply database migrations**: `python manage.py migrate`
5. **Seed sample data (optional)**: `python manage.py loaddata` if you add fixtures. The built-in itinerary generator already uses `ml_models/data/activities.csv`.
6. **Create a superuser (optional)**: `python manage.py createsuperuser`

You are now ready to build, test, or run the API.

---

## 🛠 Build Automation

The repository uses `pyproject.toml` + `setuptools` for packaging and a `Makefile` for day-to-day automation. Key targets:

- `make deps` – Dependency management (installs runtime/build deps)
- `make compile` – Byte-compiles Django apps to ensure import safety
- `make version` / `make bump-{major,minor,patch}` – Semantic version tracking via `VERSION`
- `make build` / `make package` – Produce distributable wheel + sdist under `dist/`
- `make test` – Run the Django test suite
- `make run` – Start the dev server at `http://0.0.0.0:8000`

Run `make help` for the complete command list and short descriptions.

---

## ▶️ Build, Test & Run (Step-by-Step)

| Goal | Command(s) | Notes |
| --- | --- | --- |
| Install deps | `make deps` | Upgrades `pip`, installs requirements + `build`. |
| Compile | `make compile` | Optional; helps catch syntax errors early. |
| Run tests | `make test` | Wraps `python manage.py test`. No tests yet, but the command scaffolding is ready. |
| Launch dev server | `make run` | Serves the API at `http://localhost:8000`. Stop with `Ctrl+C`. |
| Build distributables | `make build` | Emits `.tar.gz` + `.whl` artifacts in `dist/`. |

To reset artifacts, use `make clean`.

---

## 🔌 API Usage

Base URL (local): `http://localhost:8000/api/`

### 1. Generate Plans – `POST /api/plan/`

```bash
curl -X POST http://localhost:8000/api/plan/ \
  -H "Content-Type: application/json" \
  -d '{
        "region": "marrakesh",
        "budget": 1000,
        "currency": "USD",
        "lifestyle": "explorer"
      }'
```

**Response**
```json
{
  "plans": [
    {
      "id": "uuid",
      "title": "Explorer Plan 1",
      "activities": [...],
      "accommodation": {...},
      "estimated_cost": 920
    },
    {...},
    {...}
  ]
}
```

### 2. Confirm a Plan – `POST /api/confirm-trip/`

```bash
curl -X POST http://localhost:8000/api/confirm-trip/ \
  -H "Content-Type: application/json" \
  -d '{
        "region": "marrakesh",
        "budget": 1000,
        "currency": "USD",
        "lifestyle": "explorer",
        "selectedPlan": {
          "id": "uuid",
          "title": "Explorer Plan 1",
          "activities": [...],
          "accommodation": {...}
        }
      }'
```

### 3. List Confirmed Trips – `GET /api/confirmed-trips/`

```bash
curl "http://localhost:8000/api/confirmed-trips/?region=marrakesh&lifestyle=explorer"
```

Filters are optional; omit them to retrieve every stored trip.

---

## 📊 Data & Configuration

- Travel activities are stored in `ml_models/data/activities.csv`. Update this file to tweak destinations, activities, cost ranges, etc.
- Configuration defaults live in `config/settings.py`. Common overrides:
  - `ALLOWED_HOSTS` / `CORS_ALLOW_ALL_ORIGINS` for deployment.
  - `DATABASES` if you switch from SQLite to Postgres/MySQL.
  - `.env` support can be added via `python-dotenv` or similar if needed.

---

## ⚙️ Deployment

### Render / Heroku-style
1. Push code to GitHub.
2. Ensure `requirements.txt`, `Procfile`, and `runtime.txt` are present.
3. Configure a Web Service:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn config.wsgi`
4. Set environment variables (e.g., `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, database URL).

### Manual (Gunicorn)
```bash
make deps
python manage.py collectstatic --noinput
gunicorn config.wsgi --bind 0.0.0.0:8000
```

---

## 🧪 Troubleshooting

- **`ModuleNotFoundError: django`** – Run `make deps` (and activate your virtualenv if using one).
- **Migrations missing** – Execute `python manage.py migrate`.
- **Packaging errors about `license`** – Ensure you are on `setuptools>=77` or update the SPDX string in `pyproject.toml`.
- **CORS issues** – Install/enable `django-cors-headers` (already configured) and set `CORS_ALLOWED_ORIGINS` in settings/env.

---

## 📌 Notes

- All build metadata lives in `pyproject.toml`; update the version via `make bump-*`.
- Dataset updates don’t require migrations—just edit `activities.csv`.
- Remember to enable HTTPS and configure secrets before deploying to production.

---
