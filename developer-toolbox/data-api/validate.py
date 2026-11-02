"""Lightweight local integrity check for the structured source directory."""
import json
from pathlib import Path
from urllib.parse import urlparse

CATALOG = Path(__file__).with_name("catalog.json")

def load_catalog(path=CATALOG):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        raise ValueError("Invalid catalog document")
    seen = set()
    for item in data["sources"]:
        if not isinstance(item, dict):
            raise ValueError("Each entry must be an object")
        for field in ("category", "name", "url", "use", "license_notes", "kind"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"Missing or invalid {field}")
        if not item["url"].startswith("https://github.com/"):
            raise ValueError("Repository URL must use github.com HTTPS")
        if item["name"] in seen:
            raise ValueError("Duplicate repository")
        seen.add(item["name"])
        raw = item.get("example_raw_url")
        if raw is not None and (not isinstance(raw, str) or urlparse(raw).scheme != "https"):
            raise ValueError("Invalid HTTPS raw data URL")
    return data

if __name__ == "__main__":
    loaded = load_catalog()
    print(f"OK: {len(loaded['sources'])} references")
