"""
classify.py — Use Microsoft Phi-4-mini-instruct via Azure AI Foundry (Foundry IQ)
to assign a category and bilingual descriptions to each repo.
Reads data/repos.json, enriches each entry, writes back to data/repos.json.
Requires AZURE_AI_KEY in the environment.
"""

import json
import os
import time
from openai import OpenAI
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "repos.json"

CATEGORIES = ["AI Tools", "Dev Tools", "Data & Analytics", "Security", "Design & Creative"]

AZURE_ENDPOINT = "https://agentry-resource.services.ai.azure.com/openai/v1"
MODEL_NAME     = "Phi-4-mini-instruct"

SYSTEM_PROMPT = (
    "You are a helpful assistant that classifies open-source GitHub repositories. "
    "Always respond with valid JSON only — no markdown, no extra text."
)


def build_user_prompt(repo: dict) -> str:
    return f"""Classify this GitHub repository and write short descriptions.

Name: {repo['name']}
Description: {repo['description']}
Language: {repo['language']}
Topics: {', '.join(repo['topics'])}
Category hint: {repo['category_hint']}

Return JSON with exactly these fields:
{{
  "category": one of {CATEGORIES},
  "desc_en": "one sentence in English, max 20 words",
  "desc_zh": "一句話的繁體中文說明，最多30個字"
}}"""


def classify_repo(client: OpenAI, repo: dict) -> dict:
    """Call Phi-4-mini-instruct via Azure AI Foundry and return parsed classification."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": build_user_prompt(repo)},
            ],
            max_tokens=256,
        )
        raw = response.choices[0].message.content.strip()
        result = json.loads(raw)
        for key in ("category", "desc_en", "desc_zh"):
            if key not in result:
                raise ValueError(f"Missing key: {key}")
        if result["category"] not in CATEGORIES:
            result["category"] = repo.get("category_hint", "Dev Tools")
        return result
    except Exception as e:
        print(f"  [warn] classify failed for {repo['full_name']!r}: {e}")
        return {
            "category": repo.get("category_hint", "Dev Tools"),
            "desc_en":  repo.get("description", "")[:100],
            "desc_zh":  "",
        }


def main():
    if not DATA_PATH.exists():
        print(f"No data file found at {DATA_PATH}. Run fetch_repos.py first.")
        return

    with open(DATA_PATH, encoding="utf-8") as f:
        repos = json.load(f)

    if not repos:
        print("repos.json is empty — nothing to classify.")
        return

    api_key = os.environ.get("AZURE_AI_KEY")
    if not api_key:
        raise EnvironmentError("AZURE_AI_KEY is not set.")

    client = OpenAI(base_url=AZURE_ENDPOINT, api_key=api_key, timeout=25.0)

    unclassified = [r for r in repos if not r.get("desc_zh")]
    print(f"Classifying {len(unclassified)}/{len(repos)} repos with {MODEL_NAME} …")

    for i, repo in enumerate(unclassified, 1):
        print(f"  [{i}/{len(unclassified)}] {repo['full_name']}")
        classification = classify_repo(client, repo)
        repo.update(classification)
        time.sleep(0.5)

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    print(f"Saved classified data to {DATA_PATH}")


if __name__ == "__main__":
    main()
