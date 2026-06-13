"""
classify.py — Use Microsoft Phi-4-mini-instruct via Azure AI Foundry (Foundry IQ)
to assign a category and bilingual descriptions to each repo.
Requires AZURE_AI_KEY in the environment.
"""

import json
import os
import time
from pathlib import Path
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

DATA_PATH = Path(__file__).parent.parent / "data" / "repos.json"

CATEGORIES = ["AI Tools", "Dev Tools", "Data & Analytics", "Security", "Design & Creative"]

AZURE_ENDPOINT = "https://agentry-resource.services.ai.azure.com"
MODEL_NAME     = "Phi-4-mini-instruct"

SYSTEM_PROMPT = (
    "You are a helpful assistant that classifies open-source GitHub repositories. "
    "Always respond with valid JSON only — no markdown, no extra text."
)


def _safe(value: str, max_len: int = 200) -> str:
    """Truncate and strip control characters from user-supplied strings."""
    return str(value).replace("\n", " ").replace("\r", " ")[:max_len]


def build_user_prompt(repo: dict) -> str:
    name     = _safe(repo.get("name", ""), 100)
    desc     = _safe(repo.get("description", ""), 200)
    language = _safe(repo.get("language", ""), 50)
    topics   = _safe(", ".join(repo.get("topics", [])[:10]), 150)
    hint     = _safe(repo.get("category_hint", repo.get("category", "")), 50)
    return f"""Classify this GitHub repository and write short descriptions.

[REPO DATA START]
Name: {name}
Description: {desc}
Language: {language}
Topics: {topics}
Category hint: {hint}
[REPO DATA END]

Return JSON with exactly these fields:
{{
  "category": one of {CATEGORIES},
  "desc_en": "one sentence in English, max 20 words",
  "desc_zh": "一句話的繁體中文說明，最多30個字"
}}"""


def classify_repo(client: ChatCompletionsClient, repo: dict) -> dict:
    try:
        response = client.complete(
            messages=[
                SystemMessage(content=SYSTEM_PROMPT),
                UserMessage(content=build_user_prompt(repo)),
            ],
            model=MODEL_NAME,
            max_tokens=128,
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
            "category": repo.get("category_hint", repo.get("category", "Dev Tools")),
            "desc_en":  repo.get("description", "")[:100],
            "desc_zh":  repo.get("description", "")[:30],
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

    client = ChatCompletionsClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(api_key),
    )

    unclassified = [r for r in repos if not r.get("desc_zh")]
    print(f"Classifying {len(unclassified)}/{len(repos)} repos with {MODEL_NAME} …")

    for i, repo in enumerate(unclassified, 1):
        print(f"  [{i}/{len(unclassified)}] {repo['full_name']}")
        classification = classify_repo(client, repo)
        repo.update(classification)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(repos, f, ensure_ascii=False, indent=2)
        time.sleep(0.3)

    print(f"Done. Saved {DATA_PATH}")


if __name__ == "__main__":
    main()
