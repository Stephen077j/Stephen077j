import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).with_name("catalog.json")

def search(query="", category="", path=CATALOG):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    records = data.get("categories")
    if not isinstance(records, list):
        raise ValueError("Invalid catalog categories")
    seen = set()
    results = []
    for record in records:
        if not isinstance(record, dict) or not all(isinstance(record.get(k), str) and record[k].strip() for k in ("id","title","scope","upstream")):
            raise ValueError("Invalid catalog entry")
        if record["id"] in seen or not record["upstream"].startswith("https://github.com/"):
            raise ValueError("Duplicate identifier or unsafe upstream")
        seen.add(record["id"])
        if category and record["id"] != category:
            continue
        if query.casefold() in " ".join(record[k] for k in ("id","title","scope")).casefold():
            results.append(record)
    return results

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--category",default="")
    args=parser.parse_args()
    for item in search(args.query,args.category):
        print(f"{item['id']}: {item['title']}\n  {item['upstream']}\n  {item['scope']}")
