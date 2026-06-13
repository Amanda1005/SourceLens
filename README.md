# SourceLens 🔭

> AI-powered GitHub open-source discovery — updated daily, classified by Microsoft Phi-4.
> 每日自動探索 GitHub 最新開源專案，由 Microsoft Azure AI Foundry (Phi-4) 分類摘要。

🌐 **Live Demo**: [amanda1005.github.io/SourceLens](https://amanda1005.github.io/SourceLens)

---

## What is SourceLens?

SourceLens automatically discovers trending new GitHub repositories every day, classifies them into 5 categories using **Microsoft Phi-4-mini-instruct via Azure AI Foundry (Foundry IQ)**, and presents them in a bilingual (Traditional Chinese + English) web interface — with zero manual effort.

Built for the **Microsoft Agents League @ AI Skills Fest 2026** — Creative Apps track.

## Features

- 🤖 **AI Classification** — Microsoft Phi-4-mini-instruct (Azure AI Foundry / Foundry IQ)
- 🔄 **Rolling 7-Day Window** — daily fetch merges new repos, auto-removes entries older than 7 days
- 🌐 **Bilingual UI** — Traditional Chinese primary, English secondary
- 📊 **5 Categories** — AI Tools / Dev Tools / Data & Analytics / Security / Design & Creative
- ⚡ **Fully Automated** — GitHub Actions triggers every day at UTC 00:00, no manual work needed
- 🆓 **Zero Infrastructure Cost** — static site on GitHub Pages, no backend or database

## Tech Stack

| Layer | Technology |
|---|---|
| Data Source | GitHub Search API (unauthenticated, public) |
| AI Classification | Microsoft Azure AI Foundry — Phi-4-mini-instruct (Foundry IQ) |
| Automation | GitHub Actions (cron `0 0 * * *`) |
| Frontend | Vanilla HTML / CSS / JS — GitHub Pages |
| AI-Assisted Dev | GitHub Copilot |

## Architecture

```
⏰ GitHub Actions (UTC 00:00 daily)
         │
         ▼
📡 fetch_repos.py
   • Queries GitHub Search API across 5 categories (12 keyword queries)
   • Filters: created in last 7 days, stars > 1
   • Limits to 3 repos per category (15 max)
   • Merges with existing data, prunes repos > 7 days old
         │
         ▼
🤖 classify.py  ←── Azure AI Foundry (Foundry IQ)
   • Calls Microsoft Phi-4-mini-instruct for each new repo
   • Returns: category + English description + Traditional Chinese description
   • Saves after each repo (crash-safe)
         │
         ▼
💾 data/repos.json  (committed back to repo by Actions bot)
         │
         ▼
🌐 index.html  (GitHub Pages static site)
   • Fetches repos.json in browser
   • Category tabs, card grid, bilingual UI, dark theme
```

## Categories

| Category | 分類 | Search Keywords |
|---|---|---|
| 🤖 AI Tools | AI 工具 | ai agent, LLM, GPT |
| 🛠️ Dev Tools | 開發工具 | developer tool, cli tool, devtools |
| 📊 Data & Analytics | 資料分析 | data dashboard, data visualization |
| 🔒 Security | 資訊安全 | security tool, encryption |
| 🎨 Design & Creative | 設計創意 | generative art, UI design |

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
python src/classify.py      # classify with Phi-4 via Azure AI Foundry
```

### 5. Deploy to GitHub Pages
1. Push to GitHub and set repo to **public**
2. Settings → Pages → Deploy from branch `main` / root
3. Settings → Secrets → Actions → add `AZURE_AI_KEY`

The GitHub Actions workflow runs automatically every day at UTC 00:00.

## Microsoft IQ Integration

This project integrates **Foundry IQ** (Azure AI Foundry) as the intelligence layer:
- Phi-4-mini-instruct classifies each repository into the correct category
- Generates bilingual (EN + ZH-TW) descriptions grounded in actual repo metadata
- Runs as part of an automated agentic pipeline via GitHub Actions

## License

MIT
