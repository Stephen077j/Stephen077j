#!/usr/bin/env python3
"""Offline APK Resource Factory: generate a domain-specific asset preparation kit.

This tool NEVER scrapes, downloads, copies third-party assets or executes a project.
It only creates checklists/metadata. Licenses require human review.
Standard library only; Python 3.10+.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "RESOURCES_120.csv"
ASSET_DIRS = (
    "icons", "fonts", "images", "sprites", "animations", "audio",
    "music", "video", "models", "datasets", "maps", "documents", "other"
)
MANIFEST = "assets-manifest.json"

BASE_CHECKLIST = [
    "Toutes les fonctionnalités essentielles marchent en mode avion dès la première ouverture.",
    "Aucun écran ne dépend d'une URL, d'un CDN, de Google Fonts distant ou d'une authentification cloud.",
    "La base locale fonctionne sans serveur (SQLite/Room/Drift, fichiers ou équivalent).",
    "Toutes les ressources nécessaires sont embarquées ou préinstallées légalement.",
    "Les écrans d'erreur distinguent permission refusée, manque de stockage et fichier absent.",
    "Les permissions Android (micro, caméra, Bluetooth, fichiers, GPS) sont demandées au bon moment.",
    "Les sauvegardes et restaurations locales sont vérifiées, y compris après fermeture forcée.",
    "Le poids APK/AAB, l'ABI, la RAM et l'espace disque sont testés sur un téléphone réel.",
    "Les licences du code, des fontes, des voix, des musiques, des images et des datasets sont documentées.",
    "La signature Android release et la procédure d'installation sont vérifiées avant livraison client.",
]

DOMAIN_TESTS = {
    "Assets de jeux 2D/3D": "Test FPS, mode avion, rotation écran, tactile, sauvegarde progression, textures absentes.",
    "Moteurs de jeux": "Test FPS sur appareil modeste, collision, pause/reprise, contrôles tactiles.",
    "Sons et bruitages": "Test lecture audio local avec casque, volume, interruption par appel.",
    "Musiques et chants": "Test playback, navigation, droits de chaque chanson, paroles et enregistrement.",
    "Lecteurs audio": "Test lecture arrière-plan, verrouillage écran, reprise, déconnexion du casque.",
    "Studio musical et mixage": "Test latence micro, export WAV/MP3, charge CPU, taille des fichiers audio.",
    "Création et montage vidéo": "Test montage/export MP4 sans réseau, codecs, RAM, stockage, erreurs d'encodage.",
    "Études et cours hors ligne": "Test quiz, recherche locale, progression, PDF/vidéos sur un téléphone sans connexion.",
    "Contenus éducatifs": "Vérifier licences des cours; attention aux contenus NC en application commerciale.",
    "Caisse, POS et imprimantes": "Test ticket 58 mm, Bluetooth/USB, scanner, ordre de caisse et tickets annulés.",
    "Base de données locale": "Test migration, coupure pendant écriture, backup, restauration, concurrence.",
    "Cartographie, GPS et voyage": "Test GPS sans data, fonds cartographiques réellement locaux; ne pas aspirer les tuiles OSM.",
    "Santé et nutrition": "Test consentement, confidentialité, chiffrement et accès hors réseau.",
    "Réseau local et Bluetooth": "Test réseau LAN hors Internet, découverte, déconnexion et reprise.",
    "IA et reconnaissance vocale": "Test poids de modèle, permission micro, langue, CPU, délai de transcription.",
    "Moteurs IA locale": "Test compatibilité ABI, modèle embarqué, RAM, fonctionnement réel sans réseau.",
}


def load_rows():
    with CATALOG.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def select_rows(all_rows, domains):
    chosen = []
    for domain in domains:
        matches = [row for row in all_rows if row["domaine"].casefold() == domain.casefold()]
        if not matches:
            choices = ", ".join(sorted({row["domaine"] for row in all_rows}))
            raise ValueError("Domaine introuvable : " + domain + ". Choix : " + choices)
        chosen.extend(matches)
    return chosen


def make_kit(domain, rows, destination):
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Le dossier de sortie n'est pas vide. Choisir un nouveau dossier : " + str(destination))
    destination.mkdir(parents=True, exist_ok=True)
    for name in ASSET_DIRS:
        folder = destination / "assets" / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / ".gitkeep").write_text("", encoding="utf-8")

    data = {
        "schema_version": 1,
        "generated_for": domain,
        "generated_on": date.today().isoformat(),
        "description": "Inventaire des assets réellement ajoutés au projet, à renseigner manuellement.",
        "assets": [
            {
                "path": "assets/icons/example.svg",
                "source_url": "",
                "author": "",
                "license": "UNKNOWN",
                "license_evidence_url": "",
                "credit_required": "",
                "sha256": "",
                "redistribution_allowed": "UNVERIFIED"
            }
        ]
    }
    (destination / MANIFEST).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checklist = [
        "# Checklist APK 100 % hors ligne — " + domain,
        "",
        "**Un lien vers une ressource n'implique pas permission de redistribution.**",
        "",
    ] + ["- [ ] " + item for item in BASE_CHECKLIST]
    if domain in DOMAIN_TESTS:
        checklist += ["", "## Tests propres au domaine", "- [ ] " + DOMAIN_TESTS[domain]]
    (destination / "OFFLINE_CHECKLIST.md").write_text("\n".join(checklist) + "\n", encoding="utf-8")

    lines = [
        "# Kit d'application — " + domain, "",
        "Dossier créé automatiquement à partir d'un annuaire de ressources.",
        "Les fichiers d'art tiers ne sont **pas** téléchargés ni copiés : choisir et obtenir",
        "chaque fichier à sa source, avec le droit de l'incorporer dans l'application.",
        "",
        "## Ressources à examiner", "",
        "| Source | Utilité immédiate | Mode hors ligne | Licence / risque |",
        "|---|---|---|---|",
    ]
    for row in rows:
        name = row["ressource"].replace("|", "/")
        why = row["utilite_1_seconde"].replace("|", "/")
        offline = row["mode_offline"].replace("|", "/")
        licence = row["licence_et_risque"].replace("|", "/")
        lines.append(f"| [{name}]({row['url']}) | {why} | {offline} | {licence} |")
    lines += [
        "",
        "## Comment remplir ce kit",
        "",
        "1. Choisir des ressources dont la licence permet réellement la redistribution dans un APK.",
        "2. Copier dans `assets/` uniquement les fichiers autorisés, en gardant source et attribution.",
        "3. Remplacer l'exemple dans `assets-manifest.json` par une entrée réelle par asset.",
        "4. Contrôler le manifeste avec le script `prepare_offline_kit.py --audit CHEMIN_DU_KIT`.",
        "5. Intégrer les assets au vrai projet Flutter/Kotlin/Godot et tester en mode avion.",
        "6. Compiler et signer l'APK via le workflow de build propre à ce projet.",
        "",
        "**Important :** ce kit prépare des dossiers, ce n'est ni une application compilée,",
        "ni une preuve automatique de licence, ni une garantie de fonctionnement hors réseau.",
        "",
    ]
    (destination / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return len(rows)


def audit(folder):
    try:
        manifest = json.loads((folder / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("ERREUR manifeste manquant ou invalide :", exc, file=sys.stderr)
        return 2
    files = manifest.get("assets", [])
    if not isinstance(files, list):
        print("ERREUR : 'assets' doit être une liste", file=sys.stderr)
        return 2
    errors = 0
    total = 0
    for entry in files:
        path_str = entry.get("path", "")
        path = pathlib.Path(path_str)
        # Resolve prevents traversal and symlink escapes from the package root.
        root = folder.resolve()
        target = (folder / path).resolve()
        if path.is_absolute() or root not in target.parents or target == root:
            print("NON : chemin interdit", path_str)
            errors += 1
            continue
        if not target.is_file():
            print("NON : asset absent", path_str)
            errors += 1
            continue
        total += target.stat().st_size
        license_id = (entry.get("license") or "").strip()
        evidence = (entry.get("license_evidence_url") or "").strip()
        provenance = (entry.get("source_url") or "").strip()
        rights = entry.get("redistribution_allowed")
        if license_id in ("", "UNKNOWN") or not evidence or not provenance or rights != "VERIFIED_BY_USER":
            print("REVOIR LICENCE/PROVENANCE :", path_str)
            errors += 1
        expected = (entry.get("sha256") or "").strip()
        if expected:
            digest = hashlib.file_digest(target.open("rb"), "sha256").hexdigest()
            if digest != expected:
                print("NON : SHA256 incorrect", path_str)
                errors += 1
    print("Assets déclarés :", len(files))
    print("Taille de fichiers trouvés :", round(total / 1048576, 2), "MiB")
    print("Anomalies :", errors)
    if errors == 0:
        print("Inventaire de fichiers cohérent. Cela NE certifie pas les droits commerciaux.")
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Préparer les ressources d'un APK hors ligne")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="Lister les 30 domaines")
    mode.add_argument("--domain", help="Nom exact du domaine à préparer")
    mode.add_argument("--audit", help="Auditer un kit existant localement")
    parser.add_argument("--out", help="Dossier de sortie (avec --domain)")
    args = parser.parse_args()

    if args.audit:
        return audit(pathlib.Path(args.audit))
    rows = load_rows()
    if args.list:
        for domain in sorted({row["domaine"] for row in rows}):
            print(domain)
        return 0
    if not args.out:
        parser.error("--out est obligatoire avec --domain")
    try:
        selected = select_rows(rows, [args.domain])
        count = make_kit(args.domain, selected, pathlib.Path(args.out))
    except (ValueError, OSError) as exc:
        print("ERREUR :", exc, file=sys.stderr)
        return 2
    print("Kit créé :", args.out, "| sources indexées :", count)
    print("Ajouter les fichiers autorisés, compléter assets-manifest.json puis faire --audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
