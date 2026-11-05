#!/usr/bin/env python3
"""Enrich the Atlas GitHub candidate CSV via the official GitHub REST API.

Not a source-code audit. Evidence levels are explicit:
DISCOVERED_ONLY -> REPO_METADATA_MATCHED -> LICENSE_FILE_CHECKED.
No installation, cloning, arbitrary code execution, or private data extraction.
"""
import argparse
import csv
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
API = "https://api.github.com"
FIELDS = [
    "categories", "repository", "url", "search_intent", "description",
    "language", "stars", "last_push", "archived", "topics", "license_spdx",
    "license_category", "license_file_sha", "license_file_spdx",
    "license_evidence", "quality_score", "qualification", "note",
]
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
              "0BSD", "Unlicense", "CC0-1.0", "Zlib", "BSL-1.0"}
COPYLEFT = ("GPL-", "AGPL-", "LGPL-", "MPL-", "EPL-", "OSL-", "EUPL-")


def get(path, token, max_retries=2):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Stephen077j-Internet-Atlas-Curation/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    url = API + path
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            retry_after = exc.headers.get("Retry-After")
            remaining = exc.headers.get("X-RateLimit-Remaining")
            if exc.code in (403, 429) and attempt < max_retries:
                if retry_after:
                    pause = min(120, max(10, int(retry_after)))
                elif remaining == "0":
                    reset = int(exc.headers.get("X-RateLimit-Reset") or 0)
                    pause = min(180, max(10, reset - int(time.time()) + 3))
                else:
                    pause = 65
                print("Rate limit: wait", pause, "seconds", file=sys.stderr)
                time.sleep(pause)
                continue
            print("API error", exc.code, path[:90], file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print("API/network error", str(exc)[:100], file=sys.stderr)
            return None
    return None


def license_category(spdx):
    if spdx in PERMISSIVE:
        return "PERMISSIVE_CHECK_OBLIGATIONS"
    if spdx and spdx.startswith(COPYLEFT):
        return "COPYLEFT_CHECK_DISTRIBUTION_OBLIGATIONS"
    return "UNKNOWN_OR_CUSTOM_REVIEW"


def evaluate(item, metadata):
    if metadata is None:
        item.update(qualification="DISCOVERED_ONLY", quality_score="0",
                    note="Repository metadata not retrieved")
        return
    spdx = (metadata.get("license") or {}).get("spdx_id") or ""
    item.update({
        "description": (metadata.get("description") or "").replace("\n", " ")[:360],
        "language": metadata.get("language") or "",
        "stars": str(metadata.get("stargazers_count") or 0),
        "last_push": metadata.get("pushed_at") or "",
        "archived": str(bool(metadata.get("archived", False))).lower(),
        "topics": "|".join((metadata.get("topics") or [])[:15]),
        "license_spdx": spdx,
        "license_category": license_category(spdx),
        "license_evidence": "GITHUB_LICENSE_METADATA_ONLY",
    })
    stars = int(item["stars"])
    good_license = spdx not in ("", "NOASSERTION", "OTHER")
    today = dt.datetime.now(dt.timezone.utc)
    try:
        pushed = dt.datetime.fromisoformat(item["last_push"].replace("Z", "+00:00"))
        days_old = (today - pushed).days
    except (ValueError, TypeError):
        days_old = 99999
    score = (
        (30 if good_license else 0)
        + (25 if days_old <= 730 else 0)
        + (10 if days_old <= 180 else 0)
        + (15 if stars >= 50 else (8 if stars >= 10 else 0))
        + (10 if len(item["description"]) >= 20 else 0)
        + (10 if not metadata.get("archived") else 0)
    )
    item["quality_score"] = str(score)
    is_qualified = good_license and not metadata.get("archived") and days_old <= 730 and score >= 65
    item["qualification"] = "METADATA_PREQUALIFIED" if is_qualified else "REVIEW_REQUIRED"
    item["note"] = "Search relevance and safety NOT independently tested"


def output_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--license-checks", type=int, default=250)
    parser.add_argument("--max-queries", type=int, default=40)
    parser.add_argument("--search-delay", type=float, default=2.2)
    parser.add_argument("--metadata-only", action="store_true")
    args = parser.parse_args()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN is absent; request limits will be lower.", file=sys.stderr)
    with (DATA / "unique_index.csv").open(encoding="utf-8", newline="") as handle:
        initial = list(csv.DictReader(handle))
    records = {}
    query_order = []
    for row in initial:
        key = row["repository"].casefold()
        records[key] = {
            "categories": row["categories"],
            "repository": row["repository"],
            "url": row["url"],
            "search_intent": row["search_intent"],
            "license_evidence": "NOT_CHECKED",
            "qualification": "DISCOVERED_ONLY",
        }
        for query in row.get("github_queries", "").split(" | "):
            if query and query not in query_order:
                query_order.append(query)
    print("Candidates:", len(records), "searches:", len(query_order))
    matched = {}
    for count, query in enumerate(query_order[:args.max_queries], start=1):
        if count > 1:
            time.sleep(max(2.0, args.search_delay))
        params = urllib.parse.urlencode({
            "q": query, "per_page": "100", "page": "1"
        })
        payload = get("/search/repositories?" + params, token)
        if not payload:
            continue
        for obj in payload.get("items", []):
            key = (obj.get("full_name") or "").casefold()
            if key in records:
                matched[key] = obj
        print("Search", count, "matched total", len(matched))

    for key, item in records.items():
        evaluate(item, matched.get(key))

    if not args.metadata_only:
        eligible = [item for item in records.values()
                    if item["qualification"] == "METADATA_PREQUALIFIED"]
        eligible.sort(key=lambda x: (-int(x["quality_score"]), -int(x["stars"]), x["repository"]))
        for count, item in enumerate(eligible[:max(0, args.license_checks)], start=1):
            api_path = "/repos/" + "/".join(
                urllib.parse.quote(part, safe="") for part in item["repository"].split("/", 1)
            ) + "/license"
            license_data = get(api_path, token)
            if not license_data:
                item["license_evidence"] = "LICENSE_ENDPOINT_MISSING_OR_FAILED"
                continue
            file_sha = license_data.get("sha") or ""
            file_spdx = (license_data.get("license") or {}).get("spdx_id") or ""
            item["license_file_sha"] = file_sha
            item["license_file_spdx"] = file_spdx
            if file_sha and file_spdx == item["license_spdx"] and file_spdx not in ("", "NOASSERTION"):
                item["license_evidence"] = "LICENSE_FILE_CHECKED_GITHUB_API"
                item["qualification"] = "LICENSE_FILE_CHECKED"
            else:
                item["license_evidence"] = "FILE_LICENSE_MISMATCH_REVIEW"
                item["qualification"] = "REVIEW_REQUIRED"
            if count % 50 == 0:
                print("License files checked:", count)

    DATA.mkdir(parents=True, exist_ok=True)
    all_rows = sorted(records.values(), key=lambda x: (
        -int(x.get("quality_score") or 0), -int(x.get("stars") or 0), x["repository"]))
    qualified = [x for x in all_rows if x["qualification"] in
                 ("METADATA_PREQUALIFIED", "LICENSE_FILE_CHECKED")]
    license_checked = [x for x in all_rows if x["qualification"] == "LICENSE_FILE_CHECKED"]
    review = [x for x in all_rows if x["qualification"] not in
              ("METADATA_PREQUALIFIED", "LICENSE_FILE_CHECKED")]
    output_csv(DATA / "catalog_all_enriched.csv", all_rows)
    output_csv(DATA / "metadata_prequalified.csv", qualified)
    output_csv(DATA / "license_file_checked.csv", license_checked)
    output_csv(DATA / "needs_review.csv", review)

    summary = [
        "# Atlas Internet — contrôle automatique des dépôts",
        "",
        "Résultats obtenus via GitHub REST API. **La préqualification est fondée",
        "sur les métadonnées et ne constitue PAS un audit du code, des dépendances,",
        "des vulnérabilités ou du droit de redistribution commerciale.**",
        "",
        "| Mesure | Nombre |",
        "|---|---:|",
        "| Dépôts uniques en entrée | " + str(len(records)) + " |",
        "| Métadonnées retrouvées par API | " + str(len(matched)) + " |",
        "| Préqualifiés par métadonnées, fichier pas forcément lu | " + str(len(qualified)) + " |",
        "| Fichiers LICENSE contrôlés et SPDX concordant | " + str(len(license_checked)) + " |",
        "| Examen complémentaire requis | " + str(len(review)) + " |",
        "",
        "## Lire en une seconde",
        "",
        "| Projet | Domaine | Utilité recherchée | Licence GitHub | Preuve |",
        "|---|---|---|---|---|",
    ]
    for item in qualified[:100]:
        repo = item["repository"]
        purpose = (item["search_intent"] or "").split(" | ")[0].replace("|", "/")
        evidence = "fichier" if item["qualification"] == "LICENSE_FILE_CHECKED" else "métadonnées"
        summary.append("| [" + repo + "](" + item["url"] + ") | "
                       + item["categories"].replace("|", ", ") + " | " + purpose + " | "
                       + item.get("license_spdx", "") + " | " + evidence + " |")
    summary.extend([
        "", "## À vérifier avant réutilisation",
        "Licence du projet et de ses dépendances, attribution, copyleft,",
        "sécurité du code, versions maintenues, compatibilité matérielle,",
        "fonctionnalités réelles. Aucune licence ne vaut validation commerciale universelle.",
        "",
        "CSV complets : catalog_all_enriched.csv, metadata_prequalified.csv,",
        "license_file_checked.csv et needs_review.csv.",
        "",
    ])
    (DATA / "COLLECTION_REPORT.md").write_text("\n".join(summary), encoding="utf-8")
    print("DONE", json.dumps({
        "candidates": len(records), "metadata": len(matched),
        "prequalified": len(qualified), "license_file_checked": len(license_checked),
        "review_required": len(review),
    }))


if __name__ == "__main__":
    main()
