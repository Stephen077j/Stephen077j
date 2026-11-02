# FastAPI Stock Tracker

A small, independently runnable **FastAPI / Python** portfolio example by Joel Stephen. Uses sample data and no production credentials.

## Start

```bash
cd projects/fastapi-inventory/
python -m venv .venv
# Activate .venv then:
pip install -r requirements.txt
uvicorn main:app --reload
```

## Tests

Install pytest and run `pytest -q`.

## Scope and limitations

This is an educational demonstration, not a production system. The app tracks stock in memory (restarts reset data). No authentication, persistent multiuser storage, or sensitive customer records.

## Français

Projet de démonstration Python avec **FastAPI**, documentation et tests. Les données sont fictives et le logiciel n'est pas prêt à être utilisé en production.
