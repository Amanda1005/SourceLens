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

**[0:00 – 0:20] Hook**
"Every day, thousands of new open-source projects appear on GitHub. Most developers never see them. SourceLens fixes that — automatically, using Microsoft AI."

**[0:20 – 1:10] Show the live website**
- Open `amanda1005.github.io/SourceLens`
- Show the glassmorphism UI and animated background
- Click through Category tabs: AI Tools, Dev Tools, Security, Web3 / Blockchain
- Click Language tabs: JavaScript / TypeScript, Python
- Hover a card — show the 3D tilt effect
- Click "View on GitHub" on a repo
- Point to the stats bar: "AI-curated projects, updated daily"

**[1:10 – 2:00] Show the automation**
- Open GitHub repository → Actions tab
- Show the daily workflow run history
- Click a recent run, walk through the steps:
  "Fetch repos from GitHub" → "Classify with Phi-4 via Azure AI Foundry" → "Commit and push"
- "This pipeline runs every day at midnight UTC. No human clicks required."

**[2:00 – 2:40] Show the code**
- Open `fetch_repos.py` → "Six categories, each with its own search window and star threshold — AI Tools searches the last 90 days, Web3 searches a full year with 100+ stars"
- Open `classify.py` → "Each repo is sent to Microsoft Phi-4-mini-instruct via Azure AI Foundry. It returns a category and bilingual descriptions in one call."
- Open `daily.yml` → "One workflow file. GitHub handles the schedule, the secrets, and the deployment."

**[2:40 – 3:00] Closing**
"SourceLens is fully open source. It is a real agentic pipeline powered by Microsoft Azure AI Foundry — discovering, classifying, and presenting new open-source projects every single day, automatically."

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
