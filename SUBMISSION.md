# SourceLens — Submission Materials
## Microsoft Agents League @ AI Skills Fest 2026 | Creative Apps Track

---

## 📋 Project Description (for submission form)

**Project Name:** SourceLens

**One-line pitch:**
SourceLens is an AI-powered open-source discovery engine that automatically scans GitHub every day, classifies new repositories using large language models, and presents them in a bilingual (English + Traditional Chinese) web dashboard — with zero manual effort.

**Full Description (300 words):**
SourceLens solves a real problem for developers: keeping up with the explosion of new open-source projects on GitHub. With thousands of new repositories created daily, it's nearly impossible to manually find the gems.

Built entirely on GitHub infrastructure (GitHub Actions, GitHub Search API, GitHub Pages), SourceLens runs an automated daily pipeline:

1. **Discover** — A Python script queries the GitHub Search API across 17 keyword combinations covering 5 technology categories: AI Tools, Dev Tools, Data & Analytics, Security, and Design & Creative. It filters for repos created in the past 24 hours with more than 20 stars, ensuring quality signal.

2. **Classify & Describe** — Each discovered repository is sent to a large language model (Claude claude-sonnet-4-6), which assigns a category and generates both an English and Traditional Chinese description. The bilingual output makes SourceLens accessible to a global audience.

3. **Publish** — The enriched JSON data is committed back to the repository by GitHub Actions, and GitHub Pages automatically re-serves the updated static site. No backend infrastructure required.

The frontend is a single-file static web app with a polished dark-theme UI: filterable category tabs, card-based repo display, star counts, language indicators, and clickable links to GitHub.

**Key innovations:**
- Fully automated pipeline: from GitHub raw data → AI enrichment → live website, zero human intervention after deployment
- Bilingual AI-generated descriptions (Traditional Chinese + English) — rare in open-source tools
- Lightweight architecture: no database, no server, no infrastructure costs

**Developed with:** GitHub Copilot (AI-assisted development), GitHub Actions, GitHub Search API, GitHub Pages, Python, Anthropic Claude API

---

## 🏗️ Architecture Diagram Description

*Use this description to draw your diagram in draw.io / Canva / Excalidraw:*

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions                        │
│              ⏰ Triggers daily at UTC 00:00              │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  fetch_repos.py                                         │
│  • Queries GitHub Search API                            │
│  • 17 keyword queries × 5 categories                   │
│  • Filters: created last 24h, stars > 20               │
│  • Deduplicates by repo full_name                      │
└─────────────────────┬───────────────────────────────────┘
                      │ raw repo list (JSON)
                      ▼
┌─────────────────────────────────────────────────────────┐
│  classify.py                                            │
│  • Calls Claude claude-sonnet-4-6 API for each repo        │
│  • Returns: category + desc_en + desc_zh               │
│  • Enriches repos.json with AI-generated metadata      │
└─────────────────────┬───────────────────────────────────┘
                      │ enriched repos.json
                      ▼
┌─────────────────────────────────────────────────────────┐
│  data/repos.json                                        │
│  Auto-committed by GitHub Actions bot                   │
│  → triggers GitHub Pages rebuild                       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  index.html (GitHub Pages)                              │
│  • Fetches repos.json via browser fetch()              │
│  • Category tabs, card grid, bilingual descriptions    │
│  • Dark theme, responsive, XSS-safe                   │
└─────────────────────────────────────────────────────────┘
```

**Components to include in your diagram:**
- **GitHub Actions** (top, with clock icon) → trigger box
- **GitHub Search API** (left) → feeds into fetch_repos.py
- **Claude API / Anthropic** (right) → feeds into classify.py
- **repos.json** (center) → the data hub
- **GitHub Pages** (bottom) → serves to users
- **Users / Browser** (bottom right) → end consumers

**Color suggestion:**
- GitHub Actions: blue (#0366d6)
- GitHub API: gray (#24292e)
- Claude/AI: purple (#7c3aed)
- Data file: green (#2da44e)
- Frontend: orange (#e36209)

---

## 🎬 5-Minute Demo Video Script

**[0:00 – 0:30] Hook + Problem**
"Every day, hundreds of new open-source projects appear on GitHub. Most developers miss them. SourceLens fixes that automatically."

**[0:30 – 1:30] Show the live website**
- Open the GitHub Pages URL
- Show the full card grid (all repos)
- Click through category tabs: AI Tools, Dev Tools, Security…
- Point out: bilingual descriptions (中文 + English), star counts, language badges
- Hover over a card to show the animation

**[1:30 – 2:30] Show the automation**
- Open GitHub repository on GitHub.com
- Go to Actions tab → show the daily workflow run history
- Click on a recent run → walk through the steps:
  - "Fetch repos from GitHub" → "Classify repos with Claude" → "Commit and push"
- "This runs automatically every day at midnight UTC — no human clicks required"

**[2:30 – 3:30] Show the code briefly**
- Open fetch_repos.py → "17 search queries, filtering last 24h repos with stars > 20"
- Open classify.py → "Each repo gets sent to Claude, which returns category + bilingual description"
- Open daily.yml → "The whole pipeline as GitHub Actions steps"

**[3:30 – 4:30] Architecture overview**
Show your architecture diagram and narrate:
"Data flows from GitHub Search API → Python classification agent → Claude AI → JSON file → static website. Zero infrastructure costs, fully serverless."

**[4:30 – 5:00] Closing**
"SourceLens is open source. Star it on GitHub, fork it, run your own version. Built with GitHub Copilot and GitHub Actions — Microsoft's developer ecosystem made this possible."

---

## ✅ Submission Checklist

- [ ] GitHub repo is **public**
- [ ] README.md is complete (already done ✅)
- [ ] `data/repos.json` has sample data (already done ✅)
- [ ] GitHub Pages is enabled (Settings → Pages → Deploy from main branch)
- [ ] `ANTHROPIC_API_KEY` added to repo Secrets (Settings → Secrets → Actions)
- [ ] Architecture diagram image created and added to README
- [ ] Demo video recorded and uploaded to YouTube/Vimeo
- [ ] Submission form filled out with:
  - Project name: SourceLens
  - GitHub repo URL
  - Live demo URL (GitHub Pages)
  - Demo video URL
  - Track: Creative Apps
  - Description (use text from this file)

---

## 🔗 Links to prepare

- **GitHub repo:** `https://github.com/Amanda1005/SourceLens`
- **Live demo:** `https://Amanda1005.github.io/SourceLens`
- **Demo video:** *(record and upload to YouTube/Vimeo, then add URL here)*
