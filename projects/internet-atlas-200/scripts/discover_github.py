#!/usr/bin/env python3
"""Discover public GitHub repositories through the official Search API.

No authentication bypass, no code execution, no cloning, no hidden scraping.
Outputs candidate metadata only; licenses and security remain unverified.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

QUERIES = [
    ("pos", "point of sale receipt printer in:name,description,readme stars:>5"),
    ("offline", "offline first sync in:name,description,readme stars:>10"),
    ("education", "school management system in:name,description stars:>5"),
    ("ocr", "document OCR in:name,description stars:>10"),
    ("erp", "open source ERP in:name,description stars:>10"),
    ("audio", "speech recognition offline in:name,description stars:>10"),
    ("maps", "offline maps routing in:name,description stars:>10"),
    ("china", "开源 管理系统 in:description stars:>5"),
    ("japan", "オープンソース in:description stars:>5"),
    ("korea", "오픈소스 in:description stars:>5"),
]
FIELDS = ["category", "name", "url", "description", "language", "stars",
          "updated_at", "license_spdx", "archived", "status"]


def fetch(query, token, timeout=15):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": 20}
    )
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "internet-atlas-200-discovery/1.0",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="discoveries.csv")
    parser.add_argument("--max-queries", type=int, default=3)
    parser.add_argument("--delay", type=float, default=7.0)
    args = parser.parse_args()
    if not 1 <= args.max_queries <= len(QUERIES):
        parser.error("max-queries must be 1.." + str(len(QUERIES)))
    if args.delay < 1:
        parser.error("delay must be at least one second")
    token = os.getenv("GITHUB_TOKEN")
    rows = {}
    for index, (category, query) in enumerate(QUERIES[:args.max_queries]):
        if index:
            time.sleep(args.delay)
        try:
            data = fetch(query, token)
        except urllib.error.HTTPError as error:
            print("GitHub API HTTP " + str(error.code) + " — stop (no retries or bypass).", file=sys.stderr)
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            print("Network/API error: " + str(error), file=sys.stderr)
            break
        for item in data.get("items", []):
            url = item.get("html_url", "")
            if not url.startswith("https://github.com/"):
                continue
            key = item.get("full_name", "").lower()
            if not key or key in rows:
                continue
            license_obj = item.get("license") or {}
            rows[key] = {
                "category": category,
                "name": item.get("full_name", ""),
                "url": url,
                "description": (item.get("description") or "").replace("\n", " ")[:250],
                "language": item.get("language") or "",
                "stars": item.get("stargazers_count", 0),
                "updated_at": item.get("updated_at", ""),
                "license_spdx": license_obj.get("spdx_id", "UNKNOWN"),
                "archived": item.get("archived", False),
                "status": "candidate_unverified",
            }
    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows.values())
    print("Saved", len(rows), "unverified candidates to", args.output)


if __name__ == "__main__":
    main()
