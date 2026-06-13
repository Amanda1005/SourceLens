# SourceLens

> Discover the best new open-source projects on GitHub — AI-classified, 10+ stars, updated daily.

Live Demo: [amanda1005.github.io/SourceLens](https://amanda1005.github.io/SourceLens)

Built for the **Microsoft Agents League @ AI Skills Fest 2026** — Creative Apps track.

---

## What is SourceLens?

SourceLens is an automated open-source discovery engine. Every day, a GitHub Actions pipeline searches GitHub for newly created repositories, filters by quality signals (10+ stars, created within 90 days), classifies them using **Microsoft Phi-4-mini-instruct via Azure AI Foundry (Foundry IQ)**, and publishes the results to a static web interface — with zero manual effort.

## Features

- AI Classification — Microsoft Phi-4-mini-instruct (Azure AI Foundry / Foundry IQ)
- 90-Day Rolling Window — daily fetch merges new repos, auto-removes entries older than 90 days
- Dual Filtering — browse by topic category and by programming language simultaneously
- Quality Filter — only repos with 10+ stars are included
- Fully Automated — GitHub Actions triggers every day at UTC 00:00, no manual work needed
- Zero Infrastructure Cost — static site on GitHub Pages, no backend or database
- Security Hardened — safeUrl() XSS protection, prompt injection mitigation, noreferrer on all links

## Tech Stack

| Layer | Technology |
|---|---|
| Data Source | GitHub Search API (unauthenticated, public) |
| AI Classification | Microsoft Azure AI Foundry — Phi-4-mini-instruct (Foundry IQ) |
| Automation | GitHub Actions (cron `0 0 * * *`) |
| Frontend | Vanilla HTML / CSS / JS — GitHub Pages |
| Hosting | GitHub Pages (free, zero infrastructure) |

## Architecture

```
GitHub Actions (UTC 00:00 daily)
         |
         v
fetch_repos.py
   - Queries GitHub Search API with 25 keyword combinations
   - Filters: created within 90 days, 10+ stars
   - Limits 5 repos per category, deduplicates by full_name
   - Maintains rolling 90-day window (auto-prunes old entries)
         |
         v
classify.py  <--- Microsoft Azure AI Foundry (Foundry IQ)
   - Sends each new repo to Phi-4-mini-instruct
   - Returns: category + English description + Chinese description
   - Saves incrementally after each repo (crash-safe)
   - AZURE_AI_KEY stored in GitHub Secrets only
         |
         v
data/repos.json  (committed back by Actions bot)
         |
         v
index.html (GitHub Pages)
   - Glassmorphism UI with animated background
   - 3D card tilt on hover, entrance animation
   - Dual filter: topic category tabs + language tabs
   - safeUrl() XSS protection on all external links
```

## Categories

| Category | Search Keywords |
|---|---|
| AI Tools | ai agent, LLM, chatbot, RAG, fine-tuning |
| Dev Tools | CLI, vscode extension, devtools, terminal tool, code generator |
| Data & Analytics | analytics, data visualization, dashboard, pandas, jupyter |
| Security | cybersecurity, vulnerability, authentication, penetration testing, encryption |
| Design & Creative | design system, figma plugin, animation, generative art, UI components |

## Language Filter

Repos are also filterable by programming language:

| Filter | Languages Matched |
|---|---|
| JavaScript / TypeScript | JavaScript, TypeScript, CoffeeScript, Vue |
| Python | Python |
| HTML / CSS | HTML, CSS, SCSS, Sass |
| Others | Go, Rust, Java, Shell, and all others |

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Amanda1005/SourceLens.git
cd SourceLens
```

### 2. Install dependencies

```bash
pip install requests azure-ai-inference
```

### 3. Set environment variable

```bash
export AZURE_AI_KEY=your_azure_ai_foundry_key
```

### 4. Run manually

```bash
python src/fetch_repos.py   # fetch new repos from GitHub
python src/classify.py      # generate descriptions with Phi-4 via Azure AI Foundry
```

### 5. Deploy to GitHub Pages

1. Push to GitHub and set repository to public
2. Settings > Pages > Deploy from branch `main` / root
3. Settings > Secrets > Actions > add `AZURE_AI_KEY`

The GitHub Actions workflow runs automatically every day at UTC 00:00.

## Microsoft IQ Integration

This project integrates **Foundry IQ** (Azure AI Foundry) as the intelligence layer:

- Phi-4-mini-instruct classifies each repository into the correct topic category
- Generates bilingual (English + Traditional Chinese) descriptions grounded in actual repo metadata
- Runs as part of a fully automated agentic pipeline via GitHub Actions
- API key is stored exclusively in GitHub Secrets — never in source code

## Security

- URL validation: all external links are validated to `https://github.com` before rendering
- Prompt injection mitigation: user-supplied repo fields are truncated and wrapped in delimiters before being sent to the AI model
- No credentials in source code: `AZURE_AI_KEY` is stored only in GitHub Secrets
- `rel="noopener noreferrer"` on all external links

## License

MIT
