# DevCore Business Starter — modular Python primitives

Reusable **standard-library Python 3.10+** examples for common client-software needs: secure password hashing (PBKDF2 example), roles, quotation calculation, manual payment requests, queued notification payloads and private local file storage.

## Quick start

```bash
cd developer-toolbox/freelance/business-starter
python example.py
python -m unittest discover -s tests -v
```

## Modules and guarantees

| Function | What is implemented | NOT implemented |
|---|---|---|
| `hash_password`, `verify_password` | Salted PBKDF2 hashing | User accounts, MFA, login sessions, account recovery, breach protection |
| `authorize` | Minimal role/permission example | Database-backed tenant isolation or authorization middleware |
| `quote` | Decimal totals, lines, percentage tax | Local tax/legal validation, legally compliant invoices |
| `prepare_payment` | **Pending manual payment request** | Real payment API, signed webhook, refunds, settlement |
| `notification` | Validated queued **not-sent** payload | Email/SMS delivery, retries, provider authentication |
| `save_private` | Local owner-scoped write with path checks | Encrypted cloud object storage, access controlled downloads |

Use real vetted payment and messaging SDKs to implement external integrations. **Never treat a pending payment request as paid.** Preserve transaction idempotency and verify signed webhooks on the server when adding a payment provider.

### French / Français

Ce kit fournit du code réutilisable et testé pour les devis, mots de passe, permissions, fichiers et messages. Il **n'envoie pas réellement de SMS ou d'e-mails** et **n'encaisse pas de paiements**. Les données de démonstration sont fictives.

## Before client deployment

- Choose a real framework (Django/FastAPI), authentication/session provider and protected database.
- Add per-client authorization, rate limits, secrets, migrations, audit logs, backup and recovery.
- Define actual currency minor units and applicable taxes; this demo always uses two decimals and must not be assumed correct for all currencies.
- Add storage quotas, filename sanitization, malware inspection and encrypted object storage as needed.
- Integrate approved payment/email/SMS suppliers only after checking provider terms and live credentials.
- Run integration, security, concurrency and acceptance tests; never expose this demo as a public production API.
