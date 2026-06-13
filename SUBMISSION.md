# SourceLens — Submission Materials
## Microsoft Agents League @ AI Skills Fest 2026 | Creative Apps Track

---

## Project Description (for submission form)

**Project Name:** SourceLens

**One-line pitch:**
SourceLens is an AI-powered open-source discovery engine that automatically scans GitHub every day, classifies new repositories using Microsoft Phi-4-mini-instruct via Azure AI Foundry, and presents them in a bilingual web dashboard — with zero manual effort.

**Full Description (~300 words):**
SourceLens solves a real problem for developers: keeping up with the explosion of new open-source projects on GitHub. With thousands of new repositories created daily, it's nearly impossible to manually find the gems.

Built entirely on GitHub infrastructure (GitHub Actions, GitHub Search API, GitHub Pages), SourceLens runs a fully automated daily pipeline:

1. **Discover** — A Python script queries the GitHub Search API across 25 keyword combinations covering 5 technology categories: AI Tools, Dev Tools, Data & Analytics, Security, and Design & Creative. It maintains a 30-day rolling window, merging new repos while pruning outdated ones automatically.

2. **Classify & Describe** — Each newly discovered repository is sent to **Microsoft Phi-4-mini-instruct** via **Azure AI Foundry (Foundry IQ)**. The model assigns a category and generates both an English and Traditional Chinese description. This Microsoft IQ integration is the intelligence backbone of SourceLens.

3. **Publish** — The enriched JSON data is committed back to the repository by GitHub Actions, and GitHub Pages automatically serves the updated static site. No backend infrastructure required.

The frontend features glassmorphism UI design with animated light effects, 3D card tilt on hover, category + language dual filtering, and full XSS/security hardening.

**Key innovations:**
- Fully agentic pipeline: GitHub data → Microsoft Phi-4 (Foundry IQ) → live website, zero human intervention
- Dual filtering: by topic category AND programming language simultaneously
- 30-day rolling window: site is never empty, always shows recent discoveries
- Lightweight architecture: no database, no server, no infrastructure costs

**Developed with:** Microsoft Azure AI Foundry (Phi-4-mini-instruct), GitHub Actions, GitHub Search API, GitHub Pages, Python

---

## Architecture

```
⏰ GitHub Actions (UTC 00:00 daily)
         │
         ▼
📡 fetch_repos.py
   • Queries GitHub Search API (25 keyword queries across 5 categories)
   • Filters: created in last 30 days, stars ≥ 1
   • Limits 5 repos per category, deduplicates by full_name
   • Maintains rolling 30-day window (prunes old entries)
         │
         ▼
🤖 classify.py  ←── Microsoft Azure AI Foundry (Foundry IQ)
   • Sends each new repo to Phi-4-mini-instruct
   • Returns: category + English description + Traditional Chinese description
   • Saves incrementally after each repo (crash-safe)
   • AZURE_AI_KEY stored in GitHub Secrets only
         │
         ▼
💾 data/repos.json  (committed back by Actions bot)
         │
         ▼
🌐 index.html (GitHub Pages)
   • Glassmorphism UI, 3D card tilt, animated background
   • Dual filter: Category tabs + Language tabs
   • Bilingual descriptions (EN + ZH-TW)
   • safeUrl() XSS protection, noreferrer on all external links
```

---

## 5-Minute Demo Video Script

**[0:00 – 0:30] Hook**
"Every day, hundreds of new open-source projects appear on GitHub. Most developers never see them. SourceLens fixes that — automatically, using Microsoft AI."

**[0:30 – 1:30] Show the live website**
- Open `amanda1005.github.io/SourceLens`
- Show the glassmorphism UI, animated background
- Click through Category tabs: AI Tools, Dev Tools, Security…
- Click Language tabs: JavaScript / TypeScript, Python…
- Hover a card — show the 3D tilt effect
- Click "View on GitHub" on a repo

**[1:30 – 2:30] Show the automation**
- Open GitHub repository → Actions tab
- Show daily workflow run history
- Click a recent run → walk through steps:
  - "Fetch repos from GitHub" → "Classify with Phi-4 (Azure AI Foundry)" → "Commit and push"
- "This runs every day at midnight UTC. No human clicks required."

**[2:30 – 3:30] Show the code**
- Open `fetch_repos.py` → "25 search queries, 30-day rolling window"
- Open `classify.py` → "Each repo is sent to Microsoft Phi-4-mini-instruct via Azure AI Foundry"
- Show the prompt structure — bilingual output (EN + ZH-TW)
- Open `daily.yml` → the GitHub Actions pipeline

**[3:30 – 4:30] Architecture**
"Data flows: GitHub Search API → Python fetch agent → Microsoft Phi-4 (Foundry IQ) → JSON → static website. No database. No server. Zero infrastructure cost."

**[4:30 – 5:00] Closing**
"SourceLens is fully open source. It's a real agentic pipeline powered by Microsoft Azure AI Foundry — discovering, classifying, and presenting new open-source projects every single day."

---

## Submission Checklist

- [x] GitHub repo is **public** — `github.com/Amanda1005/SourceLens`
- [x] README.md complete with architecture, setup, Microsoft IQ integration section
- [x] `data/repos.json` has live data (31 repos, 30-day rolling window)
- [x] GitHub Pages enabled — `amanda1005.github.io/SourceLens`
- [x] `AZURE_AI_KEY` added to repo Secrets (Microsoft Azure AI Foundry key)
- [x] Security review complete (XSS, prompt injection, noreferrer)
- [ ] **Demo video recorded and uploaded to YouTube** ← record tonight
- [ ] **Submission form filled** ← submit before June 14 deadline

---

## Links

- **GitHub repo:** `https://github.com/Amanda1005/SourceLens`
- **Live demo:** `https://amanda1005.github.io/SourceLens`
- **Demo video:** *(add YouTube URL after recording)*
- **Microsoft IQ used:** Azure AI Foundry — Phi-4-mini-instruct (Foundry IQ)
- **Azure endpoint:** `https://agentry-resource.services.ai.azure.com`
