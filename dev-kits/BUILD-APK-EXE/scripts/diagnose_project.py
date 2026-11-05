#!/usr/bin/env python3
"""Diagnostique le projet et indique quel workflow GitHub copier.

Analyse uniquement les noms de fichiers et le package.json local.
Ne modifie rien, n'installe rien et n'execute pas le code du projet.
"""
import argparse
import json
from pathlib import Path


def scan(root: Path):
    locations = [root]
    for sub in ("app", "mobile", "desktop", "frontend", "apps/mobile", "apps/desktop", "packages/app"):
        p = root / sub
        if p.is_dir():
            locations.append(p)
    findings = []
    for path in locations:
        rel = str(path.relative_to(root)) or "."
        if (path / "pubspec.yaml").is_file():
            windows = (path / "windows").is_dir()
            android = (path / "android").is_dir()
            findings.append({
                "stack": "Flutter",
                "dossier": rel,
                "sorties": ["APK Android", "EXE Windows"],
                "modele": "templates/flutter/.github/workflows/build-apk-exe.yml",
                "diagnostic": (
                    "Pret a configurer le workflow" if windows and android
                    else "Plateformes manquantes: "
                    + ", ".join(x for x, present in (("android/", android), ("windows/", windows)) if not present)
                ),
            })
            continue
        if (path / "src-tauri").is_dir() and (path / "package.json").is_file():
            findings.append({
                "stack": "Tauri + JavaScript",
                "dossier": rel,
                "sorties": ["EXE/installeur Windows selon configuration Tauri"],
                "modele": "A preparer pour la version et la configuration Tauri de ce projet",
                "diagnostic": "Ne pas copier le modele Flutter dans un projet Tauri.",
            })
            continue
        if (path / "pyproject.toml").is_file():
            try:
                header = (path / "pyproject.toml").read_text(encoding="utf-8")[:30000]
            except OSError:
                header = ""
            if "[tool.flet]" in header:
                findings.append({
                    "stack": "Flet/Python",
                    "dossier": rel,
                    "sorties": ["APK et Windows via flet build avec configuration Flet"],
                    "modele": "Modele Flutter non directement compatible; utiliser flet build",
                    "diagnostic": "Configurer Flet et les dependances natives.",
                })
                continue
        if (path / "main.py").is_file() or (path / "requirements.txt").is_file():
            findings.append({
                "stack": "Python",
                "dossier": rel,
                "sorties": ["EXE Windows"],
                "modele": "templates/python-desktop/.github/workflows/build-python-exe.yml",
                "diagnostic": "Adapter main.py si le point d'entree porte un autre nom.",
            })
            continue
        if (path / "android").is_dir() and (
            (path / "android/app/build.gradle").is_file()
            or (path / "android/app/build.gradle.kts").is_file()
        ):
            findings.append({
                "stack": "Android natif",
                "dossier": rel,
                "sorties": ["APK Android"],
                "modele": "Necessite un workflow Gradle Android specifique",
                "diagnostic": "Un APK natif ne se convertit pas directement en EXE Windows.",
            })
            continue
        package = path / "package.json"
        if package.is_file():
            try:
                data = json.loads(package.read_text(encoding="utf-8"))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            except (OSError, ValueError, TypeError):
                deps = {}
            stack = "Electron" if "electron" in deps else "React/Vite/Node"
            findings.append({
                "stack": stack,
                "dossier": rel,
                "sorties": ["Web uniquement" if stack != "Electron" else "EXE Windows selon configuration"],
                "modele": "Necessite Tauri, Electron ou Capacitor selon la cible",
                "diagnostic": "Un projet web seul ne genere pas automatiquement APK et EXE.",
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description="Identifier les cibles de build du projet")
    parser.add_argument("project", nargs="?", default=".", help="Dossier racine du projet")
    parser.add_argument("--json", action="store_true", help="Sortie machine lisible")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error("Le dossier n'existe pas.")
    results = scan(root)
    if args.json:
        print(json.dumps({"dossier": str(root), "resultats": results}, ensure_ascii=False, indent=2))
    elif not results:
        print("Technologie non detectee. Verifier pubspec.yaml, package.json, pyproject.toml.")
    else:
        for i, item in enumerate(results, 1):
            print(f"\n{i}. {item['stack']} — {item['dossier']}")
            print("   Sorties :", ", ".join(item["sorties"]))
            print("   Modele :", item["modele"])
            print("   Conseil :", item["diagnostic"])


if __name__ == "__main__":
    main()
