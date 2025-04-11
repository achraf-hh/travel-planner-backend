# Travel Planner Backend (Django + DRF)

This is the backend for the Travel Planner App. It provides a RESTful API that receives a user's budget, travel region, and lifestyle preference, then returns customized travel plans based on real-world data. Users can also confirm and save selected travel plans.

---

## 🔧 Tech Stack

- Python 3.12
- Django 5.x
- Django REST Framework
- SQLite (for development)
- pandas (for plan generation logic)

---

## 🚀 Features

- ✅ Generate 3 travel plans tailored to:
  - Budget (with currency conversion)
  - Region (e.g., Marrakesh, Agadir)
  - Lifestyle (e.g., explorer, food_lover, comfort_seeker)
- ✅ Store confirmed trips in the database
- ✅ Filter saved trips by region or lifestyle

---

## 📁 Project Structure

```
travel-planner-backend/
│
├── ml_models/
│   └── planner.py               # Logic to generate travel plans
│
├── trips/
│   ├── views.py                 # API views
│   ├── models.py                # ConfirmedTrip model
│   ├── serializers.py           # Data serializers
│   └── urls.py                  # API endpoints
│
├── config/
│   └── settings.py              # Project settings
│
├── activities.csv               # Dataset of travel activities
├── requirements.txt
├── runtime.txt
└── Procfile
```

---

## 📦 API Endpoints

### 1. `POST /api/plan/`

Generate travel plans.

**Request Body**:
```json
{
  "region": "marrakesh",
  "budget": 1000,
  "currency": "USD",
  "lifestyle": "explorer"
}
```

**Response**:
```json
{
  "plans": [
    {
      "id": "uuid",
      "title": "Explorer Plan 1",
      ...
    },
    ...
  ]
}
```

---

### 2. `POST /api/confirm-trip/`

Confirm a selected plan and store it.

**Request Body**:
```json
{
  "region": "marrakesh",
  "budget": 1000,
  "currency": "USD",
  "lifestyle": "explorer",
  "selectedPlan": {
    "id": "...",
    "title": "...",
    "activities": [...],
    "accommodation": {...}
  }
}
```

---

### 3. `GET /api/confirmed-trips/`

Fetch confirmed trips (optionally filter by region and/or lifestyle):

Example:
```
GET /api/confirmed-trips/?region=marrakesh&lifestyle=explorer
```

---

## ⚙️ Deployment on Render

1. Push this project to GitHub.
2. Add these files:
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
3. Create a Web Service on [Render.com](https://render.com)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi`

---

## 📌 Notes

- Make sure to enable **CORS** if you're connecting with a frontend.
- Dataset is stored in `ml_models/data/activities.csv`.

---

