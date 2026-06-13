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

# Search queries mapped to a category hint for downstream classification
SEARCH_QUERIES = {
    "AI Tools": [
        "ai agent",
        "LLM",
        "claude",
        "GPT",
        "diffusion model",
    ],
    "Dev Tools": [
        "developer tool",
        "cli tool",
        "vscode extension",
        "devtools",
    ],
    "Data & Analytics": [
        "data dashboard",
        "data visualization",
        "analytics",
    ],
    "Security": [
        "security tool",
        "privacy",
        "encryption",
    ],
    "Design & Creative": [
        "generative art",
        "UI design",
        "creative coding",
    ],
}

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
HEADERS = {"Accept": "application/vnd.github+json"}


def build_date_filter() -> str:
    """Return a GitHub date qualifier for the last 24 hours."""
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    return since.strftime("%Y-%m-%d")


def search_repos(query: str, date_since: str) -> list[dict]:
    """Fetch one page of repos matching the query, created in the last 24 h with stars > 20."""
    params = {
        "q": f"{query} created:>{date_since} stars:>20",
        "sort": "stars",
        "order": "desc",
        "per_page": 30,
    }
    try:
        resp = requests.get(GITHUB_SEARCH_URL, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("items", [])
    except requests.RequestException as e:
        print(f"  [warn] GitHub API error for '{query}': {e}")
        return []


def extract_fields(item: dict, category_hint: str) -> dict:
    """Pull only the fields we care about from a raw GitHub API item."""
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
    print(f"Searching repos created after {date_since} with stars > 20 …")

    seen: set[str] = set()
    results: list[dict] = []

    for category, queries in SEARCH_QUERIES.items():
        for query in queries:
            print(f"  [{category}] query: {query!r}")
            items = search_repos(query, date_since)
            for item in items:
                full_name = item.get("full_name", "")
                if full_name and full_name not in seen:
                    seen.add(full_name)
                    results.append(extract_fields(item, category))
            time.sleep(1)  # respect GitHub rate limit

    print(f"Found {len(results)} unique repos.")
    return results


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    repos = fetch_all_repos()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
