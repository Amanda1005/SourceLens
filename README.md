# SourceLens 🔍

> An automated GitHub open-source discovery and classification hub, updated daily.
> 自動聚合、分類 GitHub 最新開源專案，每日更新。

## What is SourceLens?

SourceLens is an AI-powered open-source aggregator that automatically discovers trending GitHub repositories every 24 hours, classifies them into categories using Claude AI, and presents them in a clean, bilingual (English/Traditional Chinese) web interface.

Built for the Microsoft Agents League Hackathon 2026 — Creative Apps track.

## Features

- 🤖 **AI Classification** — Microsoft Phi-4-mini-instruct (Azure AI Foundry) auto-categorizes every repo
- 🔄 **Daily Auto-Update** — GitHub Actions runs every 24 hours
- 🌐 **Bilingual UI** — English & Traditional Chinese
- 📊 **5 Categories** — AI Tools / Dev Tools / Data & Analytics / Security / Design & Creative
- ⚡ **Zero Manual Work** — fully automated pipeline

## Tech Stack

- **Data Source**: GitHub Search API
- **AI Classification**: Microsoft Azure AI Foundry — Phi-4-mini-instruct (Foundry IQ)
- **Automation**: GitHub Actions (cron daily)
- **Frontend**: Vanilla HTML + CSS + JS (static, hosted on GitHub Pages)
- **AI-Assisted Development**: GitHub Copilot

## Architecture

```
GitHub Search API

↓

fetch_repos.py  (抓取過去24小時 stars > 20 的新專案)

↓

classify.py     (Claude API 自動分類 + 生成中英文描述)

↓

repos.json      (結構化資料)

↓

index.html      (靜態前端渲染)

↑

GitHub Actions  (每天 UTC 00:00 自動觸發)
```

## Categories

| Category | 分類 | Keywords |
|----------|------|----------|
| 🤖 AI Tools | AI 工具 | LLM, agent, GPT, claude, diffusion |
| 🛠️ Dev Tools | 開發工具 | CLI, IDE, devtools, framework |
| 📊 Data & Analytics | 資料分析 | dashboard, visualization, ETL |
| 🔒 Security | 資安 | security, privacy, encryption |
| 🎨 Design & Creative | 設計創作 | UI, design, generative art |

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Amanda1005/SourceLens.git
cd SourceLens
```

### 2. Install dependencies
```bash
pip install requests anthropic
```

### 3. Set environment variables
```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 4. Run manually
```bash
python src/fetch_repos.py
python src/classify.py
```

### 5. Deploy
Push to GitHub, enable GitHub Pages (branch: main, root folder), add `ANTHROPIC_API_KEY` to repo Secrets.

## GitHub Actions

The workflow runs daily at UTC 00:00 automatically:
- Fetches new repos from GitHub API
- Classifies with Claude API
- Commits updated `repos.json`
- GitHub Pages re-deploys automatically

## Demo

🌐 Live site: `https://Amanda1005.github.io/SourceLens`

## License

MIT