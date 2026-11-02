"""Search curated API engineering references without network access."""
import argparse
import json
from pathlib import Path

REGISTRY = Path(__file__).with_name("registry.json")

def search(query="", category="", path=REGISTRY):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = obj["entries"]
    if obj["count"] != len(entries):
        raise ValueError("Registry count mismatch")
    output = []
    for e in entries:
        if not all(isinstance(e.get(k), str) and e[k].strip() for k in ("category","name","url","role")):
            raise ValueError("Invalid entry")
        if not e["url"].startswith("https://github.com/"):
            raise ValueError("Invalid repository URL")
        if category and e["category"].casefold() != category.casefold():
            continue
        if query.casefold() in " ".join(e[k] for k in ("category","name","role")).casefold():
            output.append(e)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    items = search(args.query,args.category)
    if args.json:
        print(json.dumps(items,indent=2,ensure_ascii=False))
    else:
        for item in items:
            print(f"[{item['category']}] {item['name']}: {item['url']}")
        print(f"{len(items)} reference(s)")
