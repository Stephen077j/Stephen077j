"""Offline command-line search across the curated world registry."""
import argparse
import json
from pathlib import Path

REGISTRY = Path(__file__).with_name("world-registry.json")

def search(query="", category="", path=REGISTRY):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = obj["entries"]
    if obj["entry_count"] != len(entries):
        raise ValueError("Invalid entry count")
    results = []
    for item in entries:
        if category and item["category"] != category:
            continue
        searchable = " ".join(str(item.get(k, "")) for k in ("name", "usage", "category", "format")).casefold()
        if query.casefold() not in searchable:
            continue
        results.append(item)
    return results

def main():
    parser = argparse.ArgumentParser(description="Search the world API and data catalog")
    parser.add_argument("query", nargs="?", default="", help="Keyword: weather, countries, school, ...")
    parser.add_argument("--category", default="", help="Exact category name")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()
    results = search(args.query, args.category)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['category']}] {item['name']} — {item['documentation']}\n  {item['usage']}\n  Terms: {item['terms']}")
        print(f"\n{len(results)} source(s) found")

if __name__ == "__main__":
    main()
