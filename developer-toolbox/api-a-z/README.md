# API A–Z Toolkit — Stephen077j

A **searchable reference catalog** for designing, mocking, testing, documenting and securing APIs, from JSON Schema to deployment. **69 curated links in nine categories.** FR/EN.

## Quick start / Démarrage

```bash
cd developer-toolbox/api-a-z
python search.py "schema"
python search.py "mock"
python search.py --category "Auth & security"
python search.py --json "openapi"
python -m unittest discover -s tests -v
```

## Navigation

| Category | What you need / Utilité |
|---|---|
| JSON Schema & validation | JSON schema, typed validation, test suites |
| REST & contracts | OpenAPI specs, editors, SDK generation, contract linting |
| Event APIs | AsyncAPI, event contracts, Protocol Buffers |
| GraphQL & RPC | GraphQL, gRPC, typed RPC |
| Mocks & fake data | Local fake APIs, realistic synthetic fixtures |
| Testing & quality | Contract, integration, load and regression tests |
| Auth & security | OAuth/OIDC, security guidance, secret checks |
| Gateway & operations | Reverse proxies, metrics, observability |
| Samples & architecture | Real API descriptions, guidelines and discovery |

## An actual reusable contract example

See [examples/products.openapi.json](examples/products.openapi.json) for a small OpenAPI 3.1 specification with a JSON Schema for product responses, errors and a GET endpoint. This is a **contract illustration**, not a deployed API.

## Recommended workflow / Processus conseillé

1. Identify the domain and draft stable identifiers, endpoint names and error formats.
2. Define JSON Schema for input/output; choose OpenAPI for REST, AsyncAPI for events, or GraphQL schema when using GraphQL.
3. Generate **synthetic** fixtures; never expose client/private records.
4. Mock endpoints locally (e.g. Prism/MSW/WireMock) to build frontend independently.
5. Add schema/contract validation, integration tests, failures, permissions and load tests.
6. Add OAuth/OIDC where required; keep keys server-side; enforce quotas and least privilege.
7. Generate documentation and clients only after validating the specification.
8. Publish versioned changes, observability, deprecation policy and rollback instructions.

## Security and rights

Entries are references, not copied source, automatically installed tools, verified API endpoints or rights to reuse external code. Inspect the upstream project's **LICENSE**, latest maintenance state, API version and usage limits. Mocks must never be exposed as real payment, identity or medical services.

## Français

Ce catalogue t'évite de rechercher les mêmes outils à chaque projet. Il fournit des références et un exemple de contrat, mais il faut encore installer et tester les logiciels choisis avant toute mise en production.
