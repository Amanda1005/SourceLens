"""
fetch_repos.py — Search GitHub for repos from the past 30 days (by language)
and merge into a rolling 30-day window. Older entries are pruned automatically.
"""

import json
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "repos.json"

MAX_PER_CATEGORY = 5   # max new repos per language category per run
KEEP_DAYS        = 30  # rolling window size

# Each list entry is a GitHub language keyword for the search API
LANGUAGE_CATEGORIES: dict[str, list[str]] = {
    "JavaScript": ["javascript", "typescript"],
    "Python":     ["python"],
    "HTML":       ["html"],
    "Others":     ["go", "rust", "java", "shell"],
}

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
HEADERS = {"Accept": "application/vnd.github+json"}


def get_language_category(language: str) -> str:
    lang = (language or "").lower()
    if lang in ("javascript", "typescript", "coffeescript", "vue"):
        return "JavaScript"
    if lang == "python":
        return "Python"
    if lang in ("html", "css", "scss", "sass"):
        return "HTML"
    return "Others"


def search_repos(language_keyword: str, date_since: str) -> list[dict]:
    params = {
        "q": f"language:{language_keyword} created:>{date_since} stars:>2",
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }
    try:
        resp = requests.get(GITHUB_SEARCH_URL, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("items", [])
    except requests.RequestException as e:
        print(f"  [warn] GitHub API error for 'language:{language_keyword}': {e}")
        return []


def extract_fields(item: dict, category: str) -> dict:
    return {
        "name":        item.get("name", ""),
        "full_name":   item.get("full_name", ""),
        "description": item.get("description") or "",
        "url":         item.get("html_url", ""),
        "stars":       item.get("stargazers_count", 0),
        "language":    item.get("language") or "",
        "topics":      item.get("topics", []),
        "created_at":  item.get("created_at", ""),
        "category":    category,
    }


def fetch_new_repos() -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=30)
    date_since = since.strftime("%Y-%m-%d")
    print(f"Fetching repos created after {date_since} (last 30 days, stars > 2) …")

    seen: set[str] = set()
    results: list[dict] = []

    for category, lang_keywords in LANGUAGE_CATEGORIES.items():
        cat_count = 0
        for lang_keyword in lang_keywords:
            if cat_count >= MAX_PER_CATEGORY:
                break
            print(f"  [{category}] language:{lang_keyword}")
            items = search_repos(lang_keyword, date_since)
            for item in items:
                if cat_count >= MAX_PER_CATEGORY:
                    break
                full_name = item.get("full_name", "")
                if full_name and full_name not in seen:
                    seen.add(full_name)
                    results.append(extract_fields(item, category))
                    cat_count += 1
            time.sleep(1)

    print(f"Found {len(results)} new repos.")
    return results


def prune_old(repos: list[dict]) -> list[dict]:
    """Remove repos created more than KEEP_DAYS days ago."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)
    kept = []
    for r in repos:
        try:
            created = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
            if created >= cutoff:
                kept.append(r)
        except Exception:
            kept.append(r)
    return kept


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    existing: list[dict] = []
    if OUTPUT_PATH.exists():
        try:
            with open(OUTPUT_PATH, encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    # Re-categorize existing repos by language (migration for old category names)
    for repo in existing:
        old_cat = repo.get("category", "")
        if old_cat not in LANGUAGE_CATEGORIES:
            repo["category"] = get_language_category(repo.get("language", ""))

    new_repos = fetch_new_repos()

    # Merge: new repos first, then existing (skip duplicates)
    existing_names = {r["full_name"] for r in new_repos}
    merged = new_repos[:]
    for repo in existing:
        if repo["full_name"] not in existing_names:
            merged.append(repo)
            existing_names.add(repo["full_name"])

    merged = prune_old(merged)
    print(f"Rolling window total: {len(merged)} repos (after pruning).")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
