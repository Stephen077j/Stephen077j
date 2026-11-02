# Quote API — Python + Flask

A small, testable JSON API for calculating service quotations. Built as a practical Flask portfolio example.

## Quick start

Requires Python 3.10+.

```bash
cd projects/python-flask-quote-api
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m flask --app app run --debug
```

For local development only; do not use Flask's debug server in production.

## Endpoints

- `GET /health` → `{"status":"ok"}`
- `POST /api/quote` → validated quote totals.

Request example:

```json
{"items":[{"description":"Web maintenance","quantity":2,"unit_price":25}],"tax_percent":10}
```

Response includes line totals, subtotal, tax and total, using decimal arithmetic and string amounts.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Limits

This is a **demo**, not invoicing software: no authentication, storage, payment handling or legal tax compliance. Never send customer data to a public demo.

## Français

API REST Flask de calcul de devis : validation des données, calculs décimaux et tests unitaires. Projet pédagogique et professionnel destiné à montrer du code Python vérifiable.
