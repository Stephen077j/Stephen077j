"""Validate curated offline JSON files with Python standard library."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def validate():
    files=sorted((ROOT/"datasets").rglob("entries.json"))
    assert len(files)==5, f"expected five regional files, found {len(files)}"
    countries=set()
    total=0
    for path in files:
        obj=json.loads(path.read_text(encoding="utf-8"))
        assert obj["country"] not in countries
        countries.add(obj["country"])
        assert obj["source"]["url"].startswith("https://")
        assert obj["language"] in ("en","fr","mg","ja")
        assert obj["entries"]
        for entry in obj["entries"]:
            assert all(entry.get(k) for k in ("id","name","description","source_url","verification"))
        total+=len(obj["entries"])
    assert countries=={"US","GB","FR","JP","MG"}
    print(f"Validated {len(files)} country JSONs, {total} records")
    return total
if __name__=="__main__":validate()
