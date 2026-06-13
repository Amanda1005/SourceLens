# SourceLens — Submission Materials
## Microsoft Agents League @ AI Skills Fest 2026 | Creative Apps Track

---

## Project Description (for submission form)

**Project Name:** SourceLens

**One-line pitch:**
SourceLens is an AI-powered open-source discovery engine that automatically scans GitHub every day, classifies new repositories using Microsoft Phi-4-mini-instruct via Azure AI Foundry, and presents them in a bilingual web dashboard — with zero manual effort.

**Full Description (~300 words):**
SourceLens solves a real problem for developers: keeping up with the explosion of new open-source projects on GitHub. With thousands of new repositories created daily, it is nearly impossible to manually find the gems.

Built entirely on GitHub infrastructure (GitHub Actions, GitHub Search API, GitHub Pages), SourceLens runs a fully automated daily pipeline:

1. **Discover** — A Python script queries the GitHub Search API across 6 technology categories: AI Tools, Dev Tools, Data & Analytics, Security, Design & Creative, and Web3 / Blockchain. Each category has its own search window and star threshold, tuned to the pace of that field — from 90 days for fast-moving AI to 365 days with 100+ stars for the mature Web3 ecosystem.

2. **Classify & Describe** — Each newly discovered repository is sent to **Microsoft Phi-4-mini-instruct** via **Azure AI Foundry (Foundry IQ)**. The model assigns a category and generates both an English and Traditional Chinese description. This Microsoft IQ integration is the intelligence backbone of SourceLens.

3. **Publish** — The enriched JSON data is committed back to the repository by GitHub Actions, and GitHub Pages automatically serves the updated static site. No backend infrastructure required.

The frontend features glassmorphism UI design with animated light effects, 3D card tilt on hover, category and language dual filtering, and full XSS and security hardening.

**Key innovations:**
- Fully agentic pipeline: GitHub data → Microsoft Phi-4 (Foundry IQ) → live website, zero human intervention
- Per-category intelligence: search window and star threshold are tuned per field, not one-size-fits-all
- Dual filtering: by topic category AND programming language simultaneously
- Lightweight architecture: no database, no server, no infrastructure costs

**Developed with:** Microsoft Azure AI Foundry (Phi-4-mini-instruct), GitHub Actions, GitHub Search API, GitHub Pages, Python

---

## Architecture

```
GitHub Actions (UTC 00:00 daily)
         |
         v
fetch_repos.py
   - 6 categories, each with its own search window and star threshold
   - AI Tools: 90d / 10+ stars   |   Dev Tools: 180d / 10+ stars
   - Data & Analytics: 180d / 10+ stars   |   Design & Creative: 180d / 10+ stars
   - Security: 365d / 50+ stars   |   Web3 / Blockchain: 365d / 100+ stars
   - Deduplicates by full_name, limits 5 repos per category per run
         |
         v
classify.py  <--- Microsoft Azure AI Foundry (Foundry IQ)
   - Sends each new repo to Phi-4-mini-instruct
   - Returns: category + English description + Traditional Chinese description
   - Saves incrementally after each repo (crash-safe)
   - AZURE_AI_KEY stored in GitHub Secrets only
         |
         v
data/repos.json  (committed back by Actions bot)
         |
         v
index.html (GitHub Pages)
   - Glassmorphism UI, 3D card tilt, animated background
   - Dual filter: Category tabs + Language tabs
   - Bilingual descriptions (EN + ZH-TW)
   - safeUrl() XSS protection, noreferrer on all external links
```

---

## 3-Minute Demo Video Script

> Narration (in plain text) is what the AI voice reads.
> [Screen directions] in brackets are for the recorder only — not spoken.

---

**[0:00 – 0:20]**
[Screen: SourceLens homepage loading]

Every day, thousands of new open-source projects appear on GitHub. Most developers never find them — buried under noise, algorithm feeds, and simply too much to keep track of. SourceLens fixes that. Automatically.

---

**[0:20 – 1:15]**
[Screen: Browse the website — click category tabs, then language tabs, hover a card, click View on GitHub]

This is SourceLens — a daily open-source discovery engine, powered by Microsoft AI. Every repository you see here was discovered, classified, and described by an automated pipeline. No human curation required.

You can filter by topic: AI Tools, Dev Tools, Security, Web3 and Blockchain, and more. Or filter by programming language — JavaScript, Python, C and C-plus-plus. Both filters work at the same time, so you can narrow down to exactly what you are looking for.

Hover over any card to see the three-dimensional tilt effect. Each card shows the repository name, an AI-generated description in both English and Chinese, the programming language, and a direct link to GitHub.

---

**[1:15 – 1:55]**
[Screen: GitHub → Actions tab → click a recent workflow run]

Behind the website is a fully automated pipeline. Every day at midnight UTC, a GitHub Actions workflow runs on its own. It searches GitHub for new repositories, sends them to Microsoft Phi-4 via Azure AI Foundry for classification, and commits the results back to the repository. GitHub Pages serves the updated site instantly.

No servers. No databases. No manual work.

---

**[1:55 – 2:40]**
[Screen: fetch_repos.py → scroll to CATEGORY_CONFIG, then classify.py → scroll to build_user_prompt]

What makes SourceLens different is its per-category intelligence. AI Tools — the fastest-moving space — searches the last 90 days. Web3 and Blockchain, a more mature ecosystem, searches the past year and requires at least 100 stars. Each category is tuned to surface what actually matters in that field.

The AI layer uses Microsoft Phi-4-mini-instruct via Azure AI Foundry. For each repository, the model returns a topic category and bilingual descriptions — one in English, one in Traditional Chinese — grounded entirely in the actual repository metadata.

---

**[2:40 – 3:00]**
[Screen: Back to SourceLens homepage]

SourceLens is fully open source, built on GitHub, and powered by Microsoft Azure AI Foundry. It discovers, classifies, and publishes new open-source projects every single day — entirely on its own.

---

## Submission Checklist

- [x] GitHub repo is public — `github.com/Amanda1005/SourceLens`
- [x] README.md complete with architecture, setup, Microsoft IQ integration section
- [x] `data/repos.json` has live data
- [x] GitHub Pages enabled — `amanda1005.github.io/SourceLens`
- [x] `AZURE_AI_KEY` added to repo Secrets (Microsoft Azure AI Foundry key)
- [x] Security review complete (XSS, prompt injection, noreferrer)
- [x] MIT LICENSE included
- [ ] **Demo video recorded and uploaded to YouTube** — record today
- [ ] **Submission form filled** — submit before June 14 deadline

---

## Links

- **GitHub repo:** `https://github.com/Amanda1005/SourceLens`
- **Live demo:** `https://amanda1005.github.io/SourceLens`
- **Demo video:** *(add YouTube URL after recording)*
- **Microsoft IQ used:** Azure AI Foundry — Phi-4-mini-instruct (Foundry IQ)
- **Azure endpoint:** `https://agentry-resource.services.ai.azure.com`
