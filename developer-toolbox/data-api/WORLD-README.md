# World Data & APIs Registry — 52 sources

A searchable **offline** directory of sources useful when starting international web, mobile, AI and business projects.

## Quick use

```bash
cd developer-toolbox/data-api
python search_world.py countries
python search_world.py weather
python search_world.py --category geography
python search_world.py education --json
python -m unittest discover -s tests -v
```

The entries live in [world-registry.json](world-registry.json), grouped into nine categories: geography, internationalization, weather/earth, economy, health/education, food/media, technology, mock/testing, transport/sports.

## How to build without searching again

1. Use `search_world.py` to select candidate data sources by category.
2. Open provider documentation and verify data coverage for the exact country, especially Madagascar.
3. Verify the API's present access rules, key requirements, rate limits, license, costs and commercial usage.
4. Pin a supported endpoint version; validate response shape using JSON Schema/OpenAPI.
5. Cache approved static snapshots where legally allowed; add scheduled refresh and fallback for dynamic data.
6. Store API keys in a protected server environment, not the frontend or public repository.
7. Use synthetic data for testing and never publish client/education/health records.

### Design note

**Stable reference data** (country codes, language names, timezones) can often be cached offline with update procedures. **Live data** (weather, currencies, flight status, transport and stock) requires actual integrations and freshness checks. A GitHub list does *not* replace provider APIs, licenses, contracts or periodic updates.

### Example: search source metadata from Python

```python
from search_world import search

for provider in search("currency"):
    print(provider["name"], provider["documentation"])
```

This is not a database containing the full world or live API data. The registry stores links and metadata only. Availability of third-party endpoints has not been tested automatically.
