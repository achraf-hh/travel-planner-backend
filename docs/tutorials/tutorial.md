# Travel Planner Tutorial

This walkthrough shows how to set up the backend, generate itineraries, confirm a trip, and list saved trips.

## 1) Setup
- Create/activate a virtualenv (optional but recommended).
- Install dependencies: `pip install -r requirements.txt`
- Apply migrations: `python manage.py migrate`
- Run the dev server: `python manage.py runserver 0.0.0.0:8000`

## 2) Generate plans
Send a POST to `/api/plan/`:
```bash
curl -X POST http://localhost:8000/api/plan/ \
  -H "Content-Type: application/json" \
  -d '{"region":"Marrakesh","budget":1000,"currency":"USD","lifestyle":"explorer"}'
```
You should receive a `{"plans": [...]}` payload.

## 3) Confirm a plan
Take one plan from the previous response and POST to `/api/confirm-trip/`:
```bash
curl -X POST http://localhost:8000/api/confirm-trip/ \
  -H "Content-Type: application/json" \
  -d '{
        "region":"Marrakesh",
        "budget":1000,
        "currency":"USD",
        "lifestyle":"explorer",
        "selectedPlan":{"id":"<plan-id>","title":"My Pick","activities":[],"accommodation":{}}
      }'
```
Expect `201` with a confirmation payload.

## 4) List confirmed trips
Fetch saved trips, optionally filtered:
```bash
curl "http://localhost:8000/api/confirmed-trips/?region=Marrakesh&lifestyle=explorer"
```
You should see the trip you just confirmed.

## 5) Tests and docs (optional)
- Run tests: `python manage.py test` (or `make test`)
- Generate API docs: `make docs` and open `docs/index.html`
