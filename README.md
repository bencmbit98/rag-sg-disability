# SEN & Disability Support RAG Chatbot

A mobile-friendly Progressive Web App (PWA) that helps students with Special Educational Needs (SEN), persons with disabilities, and caregivers in Singapore find relevant support services through natural-language questions.

**Total infrastructure cost: $0.00**

---

## Live Demo

| Service | URL |
|---|---|
| Frontend (PWA) | https://tpsen-c1b69.web.app |
| Backend API | https://bencmbit98-rag-sg-disability.hf.space |
| API Docs | https://bencmbit98-rag-sg-disability.hf.space/docs |

---

## What It Does

Users ask questions in plain language (e.g. *"How do I apply for SEN support at TP?"*) and receive answers sourced directly from:

| Source | Topic |
|---|---|
| Temasek Polytechnic | SEN support for poly students |
| SG Enable | Disability transport schemes |
| SG Enable | Child & adult care services |
| SG Enable | Training & employment support |

The app uses Retrieval-Augmented Generation (RAG): it searches a local vector database of ~4,000 scraped chunks, passes the most relevant ones to an LLM, and returns a grounded answer with citations. Off-topic questions are blocked by a 3-layer guardrail system.

---

## Architecture

```
Browser (PWA)
    │
    ├── POST /query ──────► HuggingFace Space (FastAPI)
    │                           ├── Embed query (sentence-transformers)
    │                           ├── ChromaDB cosine search
    │                           ├── Guardrail: distance gate
    │                           ├── Groq LLM (llama-3.1-8b-instant)
    │                           └── Guardrail: sentinel check
    │
    └── Firestore SDK ────► Firebase (Google)
                                ├── queries/ (anonymous interaction logs)
                                └── sessions/ (session metadata)
```

---

## Features

- **RAG pipeline** — sentence-transformers embeddings + ChromaDB vector search + Groq LLM
- **3-layer guardrails** — distance gate, strict system prompt, sentinel check
- **Deep crawl** — ~110 pages scraped via Playwright/crawl4ai at build time
- **Firebase analytics** — every query logged anonymously for continuous improvement
- **Feedback widget** — thumbs up/down + optional comment per answer
- **PWA** — installable on iOS and Android via "Add to Home Screen"
- **WCAG AA** — accessible UI, keyboard navigable, aria-live regions

---

## Free & Open Source Stack — $0 Total Cost

| Layer | Technology |
|---|---|
| LLM | Groq API — `llama-3.1-8b-instant` (free) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local, no key) |
| Vector DB | ChromaDB (disk-persisted, free) |
| Scraper | crawl4ai + Playwright (open source) |
| Backend | FastAPI on HuggingFace Spaces Docker (free) |
| Frontend | Next.js 14 + Tailwind CSS (open source) |
| Hosting | Firebase Hosting (free Spark plan) |
| Analytics DB | Firestore (free Spark plan) |
| Web Analytics | Google Analytics 4 (free) |

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18.17+ (or portable zip from nodejs.org if no admin rights)
- Git

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
pip install -r requirements.txt
playwright install chromium

cp .env.example .env                # fill in GROQ_API_KEY
python -m pip install -r requirements.txt  # use python -m pip, not pip

# Run ingestion (first time only — takes ~15 min)
python scripts/ingest.py

# Start server
uvicorn app.main:app --reload --port 8000
```

> **TP network users:** Add SSL bypass env vars before running anything that makes HTTPS requests:
> ```powershell
> $env:PYTHONHTTPSVERIFY = "0"
> $env:HF_HUB_DISABLE_SSL_VERIFICATION = "1"
> $env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
> ```
> These are already patched in `app/main.py` and `scripts/ingest.py` for runtime use.

### Frontend

```bash
cd frontend
npm install
npm install firebase

# Fill in Firebase config in .env.local
cp .env.local.example .env.local    # fill in values

npm run dev                         # http://localhost:3000
```

---

## Deployment

### Backend → HuggingFace Spaces

```bash
cd backend
python scripts/deploy_to_hf.py     # patches SSL, uploads via huggingface_hub
```

- First container startup runs ingestion automatically (~15 min)
- Set `GROQ_API_KEY` and `CORS_ORIGINS` as secrets in Space Settings

### Frontend → Firebase Hosting

```bash
cd frontend
# Update NEXT_PUBLIC_API_URL in .env.local to HuggingFace Space URL
npm run build
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
firebase deploy --only hosting
```

---

## Project Structure

```
rag-sg-disability/
├── CLAUDE.md              ← AI agent instructions & architecture decisions
├── SETUP_GUIDE.md         ← Step-by-step local setup guide
├── README.md              ← This file
│
├── backend/               ← FastAPI on HuggingFace Spaces
│   ├── app/
│   │   ├── main.py        ← FastAPI app + lifespan (loads models)
│   │   ├── config.py      ← Pydantic Settings + CRAWL_SOURCES
│   │   ├── ingestion/     ← scraper, chunker, embedder
│   │   ├── retrieval/     ← ChromaDB vector search
│   │   ├── llm/           ← Groq client + system prompt
│   │   └── api/           ← routes, schemas
│   ├── scripts/
│   │   ├── ingest.py      ← Run ingestion pipeline end-to-end
│   │   └── deploy_to_hf.py← Upload to HuggingFace (SSL-patched)
│   ├── data/
│   │   ├── raw/           ← scraped markdown (gitignored)
│   │   └── chroma_db/     ← vector store (gitignored)
│   ├── Dockerfile
│   ├── start.sh           ← runs ingestion if empty, then uvicorn
│   └── requirements.txt
│
└── frontend/              ← Next.js 14 PWA on Firebase Hosting
    ├── app/               ← Next.js App Router pages
    ├── components/        ← ChatWindow, ChatBubble, SourceCard, etc.
    ├── hooks/             ← useChat, useSession
    ├── lib/               ← api.ts, firebase.ts, analytics.ts
    ├── store/             ← Zustand chat store
    └── public/            ← PWA manifest + icons
```

---

## Guardrail System

Three layers prevent the LLM from answering off-topic questions:

1. **Distance gate** — query embedding must be within `MAX_DISTANCE=0.85` of at least one indexed chunk
2. **Strict system prompt** — LLM is instructed to output `[OUT_OF_SCOPE]` if context is insufficient
3. **Sentinel check** — backend detects the sentinel and returns a friendly refusal message

---

## Firestore Analytics Schema

Every interaction is logged anonymously:

```typescript
{
  sessionId: string       // random UUID, stored in localStorage
  userMessage: string     // what the user asked
  assistantAnswer: string // what the AI answered
  sourcesUsed: string[]   // e.g. ["tp_sen", "enabling_transport"]
  sourceUrls: string[]    // exact page URLs cited
  responseTimeMs: number
  feedbackRating: 1 | 5 | null  // 👎 or 👍
  feedbackComment: string | null
  isInScope: boolean
  timestamp: Timestamp
}
```

---

## Known Issues

| Issue | Fix |
|---|---|
| TP network blocks HTTPS downloads | SSL bypass in `app/main.py` and `scripts/ingest.py` |
| `pip` points to system Python, not venv | Always use `python -m pip install` |
| Node.js requires admin to install | Use portable zip from nodejs.org, add to user PATH |
| `hf` CLI blocked by SSL on TP network | Use `scripts/deploy_to_hf.py` which patches httpx |
| Firebase CLI SSL error | Set `$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"` first |

---

## Built With

[Claude Code](https://claude.ai/claude-code) — Anthropic's AI coding agent
