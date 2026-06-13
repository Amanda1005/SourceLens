"""
fetch_repos.py — Search GitHub for trending new repos and save to data/repos.json.
Runs without a GitHub token (uses public API, 60 req/hr unauthenticated).
"""

import json
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "repos.json"

MAX_REPOS = 40  # hard cap to keep classify.py fast

SEARCH_QUERIES = {
    "AI Tools": [
        "ai agent",
        "LLM",
        "GPT",
    ],
    "Dev Tools": [
        "developer tool",
        "cli tool",
        "devtools",
    ],
    "Data & Analytics": [
        "data dashboard",
        "data visualization",
    ],
    "Security": [
        "security tool",
        "encryption",
    ],
    "Design & Creative": [
        "generative art",
        "UI design",
    ],
}

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
HEADERS = {"Accept": "application/vnd.github+json"}


def build_date_filter() -> str:
    since = datetime.now(timezone.utc) - timedelta(days=7)
    return since.strftime("%Y-%m-%d")


def search_repos(query: str, date_since: str) -> list[dict]:
    params = {
        "q": f"{query} created:>{date_since} stars:>1",
        "sort": "stars",
        "order": "desc",
        "per_page": 5,  # only top 5 per query
    }
    try:
        resp = requests.get(GITHUB_SEARCH_URL, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("items", [])
    except requests.RequestException as e:
        print(f"  [warn] GitHub API error for '{query}': {e}")
        return []


def extract_fields(item: dict, category_hint: str) -> dict:
    return {
        "name": item.get("name", ""),
        "full_name": item.get("full_name", ""),
        "description": item.get("description") or "",
        "url": item.get("html_url", ""),
        "stars": item.get("stargazers_count", 0),
        "language": item.get("language") or "",
        "topics": item.get("topics", []),
        "created_at": item.get("created_at", ""),
        "category_hint": category_hint,
    }


def fetch_all_repos() -> list[dict]:
    date_since = build_date_filter()
    print(f"Searching repos created after {date_since} with stars > 1 …")

    seen: set[str] = set()
    results: list[dict] = []

    for category, queries in SEARCH_QUERIES.items():
        for query in queries:
            if len(results) >= MAX_REPOS:
                break
            print(f"  [{category}] query: {query!r}")
            items = search_repos(query, date_since)
            for item in items:
                full_name = item.get("full_name", "")
                if full_name and full_name not in seen:
                    seen.add(full_name)
                    results.append(extract_fields(item, category))
            time.sleep(1)

    print(f"Found {len(results)} unique repos.")
    return results


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    repos = fetch_all_repos()
    if not repos:
        print("No repos found — keeping existing data.")
        return
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
