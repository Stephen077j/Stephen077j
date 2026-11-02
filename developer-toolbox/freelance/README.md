# DevCore Freelance Toolbox

A practical **FR / EN** entrypoint to start, deliver and maintain client projects without repeating research.

## Find resources

```bash
cd developer-toolbox/freelance
python search.py payment
python search.py --category 09-business-software
python -m unittest discover -s tests -v
```

The [JSON catalog](catalog.json) has 18 client-delivery categories and an upstream reference for each. These are **references**, not automatically installed packages, forked code or a guarantee of commercial permission.

## Reuse resources already on this account

| Existing project | Use case |
|---|---|
| [arena-pos-system](https://github.com/Stephen077j/arena-pos-system) | POS architecture reference; check source privacy and readiness |
| [Reservation-car](https://github.com/Stephen077j/Reservation-car) | Reservation workflow reference |
| [multivendeur](https://github.com/Stephen077j/multivendeur) | Marketplace reference |
| [CI-CD](https://github.com/Stephen077j/CI-CD) | Pipeline reference |
| [ML](https://github.com/Stephen077j/ML) | Machine learning project |
| [analyse-setiments](https://github.com/Stephen077j/analyse-setiments) | NLP learning example |
| [Python-FastAPI-Inventory](https://github.com/Stephen077j/Python-FastAPI-Inventory) | Backend starter |
| [Developer API A–Z](../api-a-z/) | JSON Schema, OpenAPI, mocks, tests and security |
| [World Data Registry](../data-api/) | Source discovery for global datasets and APIs |
| [AI Toolbox](../AI.md) | LLM, RAG, OCR, audio, MLOps |

Existing project links are navigation references; **no private/client source has been copied**.

## Client project sequence

1. **Discover:** define client, constraints, data classification, users, success metrics.
2. **Scope:** estimate features, budgets, risks, delivery plan and measurable acceptance tests.
3. **Design:** architecture, UX, auth, storage, API contract, backups and legal/data rights.
4. **Build:** incremental PRs, automated tests, staging and secure configuration.
5. **Verify:** accessibility, performance, devices, payment sandbox and user acceptance.
6. **Deliver:** deploy, document, train administrators, hand over credentials securely.
7. **Maintain:** patches, backups, incident response, SLA, invoices and support workflow.

See [project brief](templates/CLIENT-BRIEF.md), [delivery checklist](templates/DELIVERY-CHECKLIST.md) and [service README](templates/SERVICE-README.md).

## Critical caveats

- Country-specific taxes, payments, employment, privacy and invoicing require current legal/provider verification.
- Production credentials, personal data, customer software and copyrighted material must not be added to a public repo.
- Fork upstream only for a real contribution or a justified derivative; check LICENSE. Prefer install or star otherwise.
- Every proposed API needs an up-to-date review of pricing, availability, quotas and data coverage before being promised to a client.

## Français

Boîte à outils pour répondre plus vite aux demandes des clients : découvrir le besoin, sélectionner une solution, développer, tester, livrer et maintenir. Les modèles sont adaptables et ne remplacent pas une validation juridique ou technique.
