"""Offline SHA-256 directory inventory and verification; stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory(root: Path, manifest: Path) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Root must be a directory")
    manifest = manifest.resolve()
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file() or path.resolve() == manifest:
            continue
        files.append({"path": path.relative_to(root).as_posix(),
                      "size": path.stat().st_size, "sha256": digest(path)})
    return {"format": "file-integrity-lite-v1", "algorithm": "sha256", "files": files}


def verify(root: Path, data: dict) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Root must be a directory")
    if (data.get("format") != "file-integrity-lite-v1"
            or data.get("algorithm") != "sha256"
            or not isinstance(data.get("files"), list)):
        raise ValueError("Unsupported manifest format")
    errors, seen = [], set()
    for item in data["files"]:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError("Malformed manifest entry")
        name = item["path"]
        rel = PurePosixPath(name)
        if (not name or rel.is_absolute() or ".." in rel.parts
                or "\\" in name or name.startswith("./") or name in seen):
            raise ValueError("Unsafe or duplicate manifest path")
        seen.add(name)
        path = root.joinpath(*rel.parts)
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append({"path": name, "code": "unsafe_path"})
        elif not path.is_file():
            errors.append({"path": name, "code": "missing"})
        elif (not isinstance(item.get("size"), int)
              or isinstance(item.get("size"), bool)
              or path.stat().st_size != item["size"]):
            errors.append({"path": name, "code": "size_mismatch"})
        elif (not isinstance(item.get("sha256"), str)
              or len(item["sha256"]) != 64
              or any(c not in "0123456789abcdef" for c in item["sha256"])):
            raise ValueError("Malformed SHA-256 checksum")
        elif digest(path) != item["sha256"]:
            errors.append({"path": name, "code": "hash_mismatch"})
    return {"valid": not errors, "checked": len(data["files"]), "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline SHA-256 directory inventory and verification")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("create", "verify"):
        p = sub.add_parser(command)
        p.add_argument("directory", type=Path)
        p.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "create":
            data = inventory(args.directory, args.manifest)
            with args.manifest.open("x", encoding="utf-8") as out:
                json.dump(data, out, indent=2, ensure_ascii=False)
                out.write("\n")
            print("Manifest created:", args.manifest)
        else:
            data = json.loads(args.manifest.read_text(encoding="utf-8"))
            result = verify(args.directory, data)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            raise SystemExit(0 if result["valid"] else 1)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
