# JSON, datasets & APIs — Developer Toolbox

**FR:** Trouver rapidement les bons fichiers JSON, API, données de test et schémas pour les prochains projets. **EN:** Curated external developer data/API source directory.

[**Catalogue structuré JSON**](catalog.json) — machine-readable index, 17 sources, category, usage, license notes, link and source type.

## Start with the right data

| Need / Besoin | Suggested source | Important |
|---|---|---|
| Country selector, phone code, language and currency | [parseapi/lists](https://github.com/parseapi/lists) | Static JSON / CSV, publisher describes CC0 |
| Country, region, city hierarchy | [dr5hn/countries-states-cities-database](https://github.com/dr5hn/countries-states-cities-database) | Data can be large; ODbL obligations |
| Malagasy region / district / commune | [Madagascar administrative divisions](https://github.com/open-admin-data/madagascar-administrative-divisions) | Coordinates and JSON; verify source accuracy and current administrative boundaries |
| Public API discovery | [public-api-lists](https://github.com/public-api-lists/public-api-lists), [public-apis](https://github.com/public-apis/public-apis) | Each API's auth, quota, cost and terms vary |
| Sample REST backend | [JSON Server](https://github.com/typicode/json-server) | Locally mock a REST service; synthetic data only |
| Fake users, products, addresses for tests | [Faker](https://github.com/faker-js/faker) | Synthetic, not actual customer profiles |
| Browser API mocking | [MSW](https://github.com/mswjs/msw) | Test API behavior offline |
| JSON document validation | [SchemaStore](https://github.com/SchemaStore/schemastore), [JSON Schema Test Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite) | Schemas and conformance tests, not business data |
| API contract / API docs | [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification), [Redoc](https://github.com/Redocly/redoc) | Version the API contract with the code |
| Public holidays | [Nager.Date](https://github.com/nager/Nager.Date) | Verify country support and provisional holiday dates |
| Global dataset discovery | [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets) | License must be checked for each dataset |

## Real example: fetch a country list

JavaScript (browser or Node 18+):

```js
const url = "https://raw.githubusercontent.com/parseapi/lists/main/countries/countries.json";
const response = await fetch(url);
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const countries = await response.json();
console.log(countries.slice(0, 3));
```

Python 3.10+:

```python
import json
from urllib.request import urlopen

url = "https://raw.githubusercontent.com/parseapi/lists/main/countries/countries.json"
with urlopen(url, timeout=10) as response:
    countries = json.load(response)
print(countries[:3])
```

**Production:** pin to a specific upstream commit or store an approved and attributed local snapshot. Add fallback/cache, data validation and updates. Raw GitHub URLs are not a guaranteed production data API.

## Real example: mock your own products REST API

Install and run a supported release of [JSON Server](https://github.com/typicode/json-server), then use a local `db.json` such as:

```json
{
  "products": [
    {"id": "p1", "name": "Sample notebook", "price": 12000, "currency": "MGA", "stock": 4},
    {"id": "p2", "name": "Sample keyboard", "price": 85000, "currency": "MGA", "stock": 7}
  ]
}
```

Use fake data in public repos. Real payments, academic records, addresses and personal identifiers require private protected storage.

## Your project → recommended sources

- **ARENAH / shops / POS:** currencies, tax *reference only*, mock products and API response schemas; commercial prices and local tax rules must come from authoritative business sources.
- **EDUVERSE:** Madagascar divisions, ISO country/currency lists, test student records (fake only), school calendar as institution-configured data.
- **MADA GO / transport:** geographic reference lists, verified maps/geocoding provider APIs with suitable licenses and coverage.
- **AI projects:** lawful, consented datasets and evaluation splits; datasets lists are directories, not automatic permissions.
- **International forms:** countries, currencies, languages and timezones; never assume all country/location records are complete.

## What to check before reusing data / Avant de copier

1. Verify source URL, file schema, maintainer and latest update.
2. Confirm **dataset license** separately from repository code license; note attribution and share-alike.
3. Review country/region relevance, currency freshness, administrative changes, API quotas, CORS, keys and privacy.
4. Keep canonical identifiers (ISO / IANA where applicable), never use display name as database key.
5. Pin version, validate JSON, cache responsibly, record provenance and plan for missing fields.
6. Keep all API keys server-side; avoid exposing personal or customer data.

## Validate the catalog

```bash
cd developer-toolbox/data-api
python -m unittest discover -s tests -v
```

The validation tests check index shape, stable source names, HTTPS links and duplicates; they **do not** test live third-party API availability or guarantees of completeness.
