# DevCore Client Platform — reference FastAPI backend

**Python · FastAPI · SQLite · basic accounts · invoices · manual payments · email adapter · private files**

## Run / Démarrer

Python 3.11+:

```bash
cd developer-toolbox/freelance/web-platform
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
export DEVCORE_ADMIN_USER=admin
export DEVCORE_ADMIN_PASSWORD='a-unique-very-long-admin-password'
export DEVCORE_DB=./local.sqlite3
python bootstrap.py
unset DEVCORE_ADMIN_PASSWORD
uvicorn app:app --host 127.0.0.1 --port 8000
```

On Windows PowerShell, use `$env:VARIABLE='value'` instead of `export`. Navigate to `http://127.0.0.1:8000/docs` to inspect the API.

## Run tests / Tester

```bash
python -m unittest discover -s tests -v
```

## Implemented

- Login/logout with random server-side bearer tokens stored only as SHA-256 digests, session expiry, role checks, PBKDF2 hashed passwords.
- SQLite tables for users, sessions, invoices, pending manual payments, queued notifications, private-file metadata and audit.
- Invoice draft computations with `Decimal`, illustrative sequential `DEMO-` numbering, issuance history and configurable percent.
- Pending manual payments with single administrative confirmation and an audit entry; **no banking transaction or settlement verification**.
- SMTP email send adapter, executed only with valid server-side `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM`. SMS provider not configured.
- Local 1 MB private object storage with unpredictable object keys and owner-gated metadata.

## Essential limitations before delivering to a real client

**This is a tested reference, not complete production software.** No public launch until security and legal review.

- **Madagascar e-invoicing:** invoice fields and tax rates cannot be legally certified by this demo. Confirm the applicable Code des procédures fiscales, 2025 e-invoicing decrees and 2026 regulations. The numbering `DEMO-` is expressly not certified. Mandatory seller/buyer fields, paper rules, registration, and the national e-invoice system may apply; contact a Malagasy accountant.
- **Payments:** only manual recording. To integrate MVola / Orange Money / Airtel Money or intermediary Papi/Efaina/Alefa, obtain merchant permission and official API credentials, build server-side initiation, verified webhook signatures, idempotency/reconciliation and sandbox tests. Never treat requests as paid.
- **Notifications:** SMTP works only when configured and tested against the actual provider. SMS is queued but **not delivered**; delivery retries/outbox and consent checks are missing.
- **Identity:** add refresh-token rotation, brute-force prevention, MFA, reset, registration by invitation, session/device management and tenant isolation before production.
- **File storage:** add authenticated download, MIME validation, malware scanning, quotas, encryption and S3-compatible object storage for scale.
- **Database/deployment:** add versioned migrations, PostgreSQL production option, encrypted backups and restores, rate limiting, TLS, reverse proxy, monitoring and E2E tests.
- **Privacy:** all test accounts and examples must remain fictitious; never commit real credentials, customer invoices, client databases or private files.

## Documentation sources

- [MVola Developer](https://developer.mvola.mg/) — authorization, sandbox and production conditions.
- [Papi payment developer guide](https://docs.papi.mg/fr/docs/developper-guide/application-management/) — API key and signed notification configuration.
- [Madagascar DGI](https://portal.impots.mg/) — tax and invoicing legal references.

## Français

Ce modèle propose une vraie API locale avec SQLite et des tests. **Il n'encaisse pas réellement d'argent, n'envoie pas de SMS et ne garantit pas la conformité fiscale.** L'intégration réelle dépend des autorisations et comptes fournisseurs de chaque client.
