#!/usr/bin/env python3
"""Build a repeatable literature search plan from a topic and database list."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote_plus


DEFAULT_DATABASES = ["open-access", "CNKI", "SPE OnePetro", "Web of Science", "ScienceDirect", "Google Scholar"]


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def query_variants(topic: str, languages: str) -> dict[str, list[str]]:
    zh = [
        topic,
        f"{topic} 渗流机理",
        f"{topic} 复杂渗流",
        f"{topic} 气藏开发",
    ]
    en_seed = topic
    en = [
        en_seed,
        "carbonate gas reservoir complex flow mechanism",
        "carbonate gas reservoir seepage mechanism",
        "carbonate reservoir gas flow porous media",
        "fractured carbonate gas reservoir flow mechanism",
    ]
    if "中文" in languages and "英文" not in languages:
        return {"zh": zh, "en": []}
    if "英文" in languages and "中文" not in languages:
        return {"zh": [], "en": en}
    return {"zh": zh, "en": en}


def search_url(database: str, query: str) -> str:
    encoded = quote_plus(query)
    db = database.lower()
    if db == "cnki":
        return f"https://kns.cnki.net/kns8s/defaultresult/index?kw={encoded}"
    if "onepetro" in db:
        return f"https://onepetro.org/search-results?page=1&q={encoded}"
    if "science" in db and "direct" in db:
        return f"https://www.sciencedirect.com/search?qs={encoded}"
    if "web of science" in db or db == "wos":
        return "https://www.webofscience.com/wos/woscc/basic-search"
    if "google scholar" in db:
        return f"https://scholar.google.com/scholar?q={encoded}"
    if "open" in db:
        return f"https://api.openalex.org/works?search={encoded}"
    return ""


def build_plan(args: argparse.Namespace) -> dict:
    databases = split_csv(args.databases) or DEFAULT_DATABASES
    variants = query_variants(args.topic, args.languages)
    plan = {
        "topic": args.topic,
        "target_count": args.target_count,
        "year_range": args.year_range,
        "languages": args.languages,
        "databases": databases,
        "queries": variants,
        "routes": [],
        "notes": [
            "Use authorized access only.",
            "Pause at CAPTCHA, Cloudflare, SSO, 2FA, payment, or explicit access confirmation.",
            "Prefer PDF and RIS/BibTeX exports; do not treat CAJ as a Zotero-ready PDF.",
        ],
    }
    for database in databases:
        lang_queries = variants["zh"] if database.lower() == "cnki" else variants["en"] or variants["zh"]
        for query in lang_queries:
            plan["routes"].append(
                {
                    "database": database,
                    "query": query,
                    "url": search_url(database, query),
                    "status": "planned",
                }
            )
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a database search plan JSON file.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--target-count", type=int, default=20)
    parser.add_argument("--year-range", default="")
    parser.add_argument("--languages", default="中文,英文")
    parser.add_argument("--databases", default="")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_plan(args), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
