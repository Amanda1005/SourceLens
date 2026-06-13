"""
classify.py — Use Microsoft Phi-4-mini-instruct via Azure AI Foundry (Foundry IQ)
to generate bilingual descriptions for each repo.
Category is already set by fetch_repos.py (language-based); only descriptions are generated here.
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

AZURE_ENDPOINT = "https://agentry-resource.services.ai.azure.com"
MODEL_NAME     = "Phi-4-mini-instruct"

SYSTEM_PROMPT = (
    "You are a helpful assistant that writes concise descriptions for open-source GitHub repositories. "
    "Always respond with valid JSON only — no markdown, no extra text."
)


def build_user_prompt(repo: dict) -> str:
    return f"""Write short descriptions for this GitHub repository.

Name: {repo['name']}
Description: {repo['description']}
Language: {repo['language']}
Topics: {', '.join(repo['topics'])}

Return JSON with exactly these fields:
{{
  "desc_en": "one sentence in English, max 20 words",
  "desc_zh": "一句話的繁體中文說明，最多30個字"
}}"""


def classify_repo(client: ChatCompletionsClient, repo: dict) -> dict:
    """Call Phi-4-mini-instruct and return desc_en + desc_zh."""
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
        for key in ("desc_en", "desc_zh"):
            if key not in result:
                raise ValueError(f"Missing key: {key}")
        return result
    except Exception as e:
        print(f"  [warn] classify failed for {repo['full_name']!r}: {e}")
        desc = repo.get("description", "")
        return {
            "desc_en": desc[:100],
            "desc_zh": desc[:30],
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

    unclassified = [r for r in repos if not r.get("desc_en")]
    print(f"Generating descriptions for {len(unclassified)}/{len(repos)} repos with {MODEL_NAME} …")

    for i, repo in enumerate(unclassified, 1):
        print(f"  [{i}/{len(unclassified)}] {repo['full_name']}")
        result = classify_repo(client, repo)
        repo["desc_en"] = result["desc_en"]
        repo["desc_zh"] = result["desc_zh"]
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(repos, f, ensure_ascii=False, indent=2)
        time.sleep(0.3)

    print(f"Done. Saved {DATA_PATH}")


if __name__ == "__main__":
    main()
