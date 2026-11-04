"""Offline CSV schema and data-quality checks; Python 3.10+, stdlib only."""
import argparse
import csv
import json
from pathlib import Path

def validate(path: Path, required: list[str], unique: list[str] | None = None) -> dict:
    """Return a deterministic JSON-ready report without exposing row values."""
    unique = unique or []
    if len(set(required)) != len(required) or len(set(unique)) != len(unique):
        raise ValueError("Duplicate column names in schema")
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, strict=True)
        header = next(reader, [])
        if not header:
            return {"valid": False, "rows": 0, "errors": [{"line": 1, "code": "missing_header"}]}
        errors = []
        if len(set(header)) != len(header):
            errors.append({"line": 1, "code": "duplicate_header"})
        missing = sorted(set(required + unique) - set(header))
        for column in missing:
            errors.append({"line": 1, "code": "missing_column", "column": column})
        positions = {name: header.index(name) for name in set(required + unique) if name in header}
        seen = {name: set() for name in unique if name in positions}
        count = 0
        for row in reader:
            count += 1
            line = reader.line_num
            if len(row) != len(header):
                errors.append({"line": line, "code": "column_count"})
                continue
            for column in required:
                if column in positions and not row[positions[column]].strip():
                    errors.append({"line": line, "code": "empty_required", "column": column})
            for column in unique:
                if column in positions:
                    value = row[positions[column]]
                    if value in seen[column]:
                        errors.append({"line": line, "code": "duplicate_value", "column": column})
                    seen[column].add(value)
    return {"valid": not errors, "rows": count, "errors": errors}

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate CSV headers, required values and uniqueness offline")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--required", nargs="+", required=True)
    parser.add_argument("--unique", nargs="*", default=[])
    args = parser.parse_args()
    try:
        report = validate(args.csv_file, args.required, args.unique)
    except (OSError, csv.Error, UnicodeError, ValueError) as exc:
        report = {"valid": False, "rows": 0, "errors": [{"code": "input_error", "detail": str(exc)}]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["valid"] else 1)

if __name__ == "__main__":
    main()
