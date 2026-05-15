# QH HQ

A live, agentic operations terminal for Qualified Health's Office of CEO.

Built by [Justin Fink](https://justinryanventures.com) for the Strategy & Ops MBA Intern application at Qualified Health.

## What this is

A multi-panel terminal that fuses (a) live external signal monitored by a small agent fleet against (b) Qualified Health's actual public initiative + customer + competitor + regulator map. Every visible piece is grounded in real public research; the relationship-dynamics layer (headwinds / tailwinds / QH leverage / QH exposure / watch signals) is the substrate the implication-mapping agent reasons against.

The artifact is the AI-Transformation pillar of the JD, executed: a specific Office-of-CEO function (continuous external signal monitoring + QH-specific implication reasoning + watchlist-driven recommendation), prototyped end-to-end on real data.

## Architecture

```
                     ┌──────────────────────────────────────────────┐
                     │  Frontend · Next.js 16 · Tailwind v4         │
                     │  (Vercel)                                    │
                     │  Multi-panel terminal · SSE live trace       │
                     └───────────────┬──────────────────────────────┘
                                     │
                              ┌──────▼─────────────────────────────┐
                              │  Backend · FastAPI · Python 3.13   │
                              │  (Railway)                         │
                              │                                    │
                              │  Agent fleet:                      │
                              │   · news_scout (Haiku)             │
                              │   · implication_mapper (Opus)      │
                              │                                    │
                              │  Sources: RSS · SEC EDGAR ·        │
                              │   ClinicalTrials.gov · GitHub      │
                              └──────┬─────────────────────────────┘
                                     │
                       ┌─────────────▼──────────────┐
                       │  Supabase · Postgres 17    │
                       │  pgvector · 1024-dim       │
                       │  Realtime · Auth           │
                       └────────────────────────────┘
```

## Stack

| Layer       | Choice                              | Why |
|-------------|-------------------------------------|------|
| Frontend    | Next.js 16 + React 19 + Tailwind v4 | Latest production stack; deploy story is Vercel one-click. |
| Backend     | Python FastAPI + asyncio            | Anthropic Python SDK has the most mature tool-use surface; FastAPI gives async + SSE first-class. |
| DB          | Supabase Postgres + pgvector        | One service for relational data + vector search + realtime. |
| Embeddings  | Voyage-3-large (Voyage AI) or BAAI/bge-large-en-v1.5 (local FastEmbed fallback) | Both 1024-dim; Voyage if key configured, FastEmbed if not. |
| LLM         | Claude Opus 4.7 (reasoning) + Claude Haiku 4.5 (triage) | Opus for executive-prose implications; Haiku for fast relevance filtering. |
| Cron        | GitHub Actions                      | Free, simple, observable. |
| Deploy      | Vercel (frontend) + Railway (backend) | Both have first-class Next.js / Dockerfile support. |

## Local development

```bash
# Backend
cd backend
python -m venv .venv && source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # fill in keys
python -m app.data.seed_runner    # seed with research-grounded data
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev  # opens on :3000
```

## Required environment variables

### Backend
- `ANTHROPIC_API_KEY` — for agent runs
- `SUPABASE_URL` — your Supabase project URL
- `SUPABASE_SERVICE_KEY` — service role key (or anon key with RLS disabled for demo)
- `VOYAGE_API_KEY` — optional; falls back to local FastEmbed

### Frontend
- `NEXT_PUBLIC_API_URL` — backend URL (default `http://localhost:8000`)

## Deployment

### Backend → Railway
```bash
cd backend
railway init
railway up
# Then in Railway dashboard, set env vars listed above.
```

### Frontend → Vercel
```bash
cd frontend
vercel
# Then set NEXT_PUBLIC_API_URL to your Railway backend URL.
```

### Cron via GitHub Actions
Already configured at `.github/workflows/daily-news-scout.yml`. Set the secret `QH_HQ_BACKEND_URL` in your repo to your Railway backend URL.

## Research substrate

This project is built on ~24,000 words of grounded research compiled by parallel research agents:

- **`research/01-qualified-health-dossier.md`** — 5,883 words on QH itself: founding, leadership, funding, customers, partnerships, products, recent news, NBL signals.
- **`research/02-competitive-landscape.md`** — 6,007 words mapping competitors, adjacent vendors, big-tech, foundation models, recent funding, strategic patterns.
- **`research/03-regulatory-landscape.md`** — 4,508 words on FDA / CMS / state law / ONC HTI-1 / CHAI / Joint Commission / HIPAA / EU AI Act.
- **`research/04-customer-landscape.md`** — 7,902 words on 32 IDNs, 12 pharma sponsors, payers, ASCs, specialty MSOs — with named CMIOs/CDOs/CAIOs.

The V0.2 seed data in `backend/app/data/` distills this into:
- 41 organizations (customers, prospects, competitors, partners, regulators)
- 58 named contacts (publicly disclosed executives and GTM-relevant leaders)
- 25 strategic initiatives (NBLs, core platform work, partnerships, GTM motions, and internal ops)
- 18 workstream entries
- 15 seed signals + 15 hand-crafted implications

The relationship dynamics layer (`seed_dynamics.py`) is the substrate the implication-mapper agent reasons against — every org has explicit `tailwinds`, `headwinds`, `qh_leverage`, `qh_exposure`, `watch_signals` so the agent can produce defensible, specific implications instead of generic ones.

## License

MIT (open source — see footer of the deployed terminal for context).
